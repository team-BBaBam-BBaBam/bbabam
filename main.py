import bbabam.models as models
import bbabam.modules as modules
import time


class TimeCheker:
    def __init__(self) -> None:
        self.__s_time = None
        self.__e_time = None

    def __clear(self):
        self.__s_time = None
        self.__e_time = None

    def start(self):
        self.__s_time = time.time()

    def end(self):
        self.__e_time = time.time()
        print()
        dur = self.__e_time - self.__s_time
        print()
        self.__clear()
        return dur


class TokenTracker:
    def __init__(self) -> None:
        self.total_tokens = {
            "gpt-3.5-turbo": {
                "prompt_tokens": 0.0,
                "completion_tokens": 0.0,
            },
            "gpt-3.5-turbo-16k": {
                "prompt_tokens": 0.0,
                "completion_tokens": 0.0,
            },
            "gpt-3.5-turbo-0613": {
                "prompt_tokens": 0.0,
                "completion_tokens": 0.0,
            },
            "gpt-3.5-turbo-16k-0613": {
                "prompt_tokens": 0.0,
                "completion_tokens": 0.0,
            },
            "gpt-4": {
                "prompt_tokens": 0.0,
                "completion_tokens": 0.0,
            },
            "gpt-4-32k": {
                "prompt_tokens": 0.0,
                "completion_tokens": 0.0,
            },
            "gpt-4-0613": {
                "prompt_tokens": 0.0,
                "completion_tokens": 0.0,
            },
            "gpt-4-32k-0613": {
                "prompt_tokens": 0.0,
                "completion_tokens": 0.0,
            },
            "text-embedding-ada-002": {
                "prompt_tokens": 0.0,
                "completion_tokens": 0.0,
            },
        }
        self.price_per_1k = {
            "gpt-3.5-turbo": {
                "prompt_token_cost": 0.0015,
                "completion_token_cost": 0.002,
                "max_tokens": 4096,
            },
            "gpt-3.5-turbo-0613": {
                "prompt_token_cost": 0.0015,
                "completion_token_cost": 0.002,
                "max_tokens": 4096,
            },
            "gpt-3.5-turbo-16k-0613": {
                "prompt_token_cost": 0.003,
                "completion_token_cost": 0.004,
                "max_tokens": 16384,
            },
            "gpt-4-0314": {
                "prompt_token_cost": 0.03,
                "completion_token_cost": 0.06,
                "max_tokens": 8192,
            },
            "gpt-4-0613": {
                "prompt_token_cost": 0.03,
                "completion_token_cost": 0.06,
                "max_tokens": 8191,
            },
            "gpt-4-32k-0314": {
                "prompt_token_cost": 0.06,
                "completion_token_cost": 0.12,
                "max_tokens": 32768,
            },
            "gpt-4-32k-0613": {
                "prompt_token_cost": 0.06,
                "completion_token_cost": 0.12,
                "max_tokens": 32768,
            },
        }

    def add_tokens(self, model: str, prompt_tokens: float, completion_tokens: float):
        if model not in self.total_tokens:
            raise ValueError(f"{model}은(는) 유효한 모델 이름이 아닙니다.")
        self.total_tokens[model]["prompt_tokens"] += prompt_tokens
        self.total_tokens[model]["completion_tokens"] += completion_tokens

    def print_tokens(self) -> None:
        for model, tokens in self.total_tokens.items():
            print(f"Model: {model}")
            print(f"Prompt Tokens: {tokens['prompt_tokens']}")
            print(f"Completion Tokens: {tokens['completion_tokens']}")
            print("\n")

    def get_total_cost(self) -> float:
        total_cost = 0.0
        for model, tokens in self.total_tokens.items():
            price_info = self.price_per_1k[model]
            prompt_cost = price_info["prompt_token_cost"]
            completion_cost = price_info["completion_token_cost"]
            total_cost += (
                prompt_cost * tokens["prompt_tokens"]
                + completion_cost * tokens["completion_tokens"]
            )
        return total_cost


class Agent:
    def __init__(self) -> None:
        self.keywords_generator = models.KeywordGenerator()
        self.restriction_generator = models.RestrictionInformationGenerator()
        self.result_generator = models.ResultGenerator()

        self.chunk_divisor = modules.ChunkDivisor()
        self.crawler = modules.SocialCrawl()

        self.chat_history = []
        self.time_checker = TimeCheker()
        self.total_time = 0.0
        self.token_tracker = TokenTracker()

    def log(self, text):
        print()
        print("-" * 10, text, "-" * 10)
        print()

    def forward_model(self, model, inp, calc_token=True):
        self.log(model)
        self.time_checker.start()

        data, chat_hist, token_info = model.forward(inp)
        if calc_token:
            self.token_tracker.add_tokens(
                model.model,
                token_info["prompt_tokens"],
                token_info["completion_tokens"],
            )
            print("Token useage :")
            print(token_info)
        self.chat_history.append(chat_hist)
        dur = self.time_checker.end()
        print("Time Elapsed:", str(dur), "seconds")
        print()

        self.total_time += dur
        return data

    def run(self):
        search_text = input("Input Text : ")

        wlist = self.forward_model(self.keywords_generator, search_text)
        print(wlist)

        context = self.forward_model(self.crawler, wlist[:2], calc_token=False)
        context = [content["Contents"][:3] for content in context]
        print(str(context)[:300])

        restriction = self.forward_model(self.restriction_generator, search_text)
        print(restriction)

        output = self.forward_model(
            self.result_generator,
            {
                "search_text": search_text,
                "restriction": restriction,
                "information": str(context),
            },
        )

        print(output)
        print("Total :", self.total_time, "seconds")

        print("Token Usage :")
        self.token_tracker.print_tokens()


if __name__ == "__main__":
    agent = Agent()
    agent.run()
