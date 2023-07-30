from .base_model import ChatModel
from typing import Dict

RESULT_GENERATOR_PROMPT = """
            Now, you should output overall conclusion according to previous chat.
            Tell me proper information considering previous chat such as my first input, and keyword and restriction you generated, and the result of searched social data.
            Tell me in language when I firstly input my request that I wanted to know.
            Use searched(given) information rather than your pre-trained insight.
            You should combine overall informations given, and answer it in 400 letters.

            Moreover, tell me the source of your inference by NAVER blog urls.


"""


class ResultGenerator(ChatModel):
    def __init__(
        self,
        model_type: str = "gpt-3.5",
        temperature: float = 0.2,
        stable: bool = True,
        more_tokens: bool = True,
    ):
        super().__init__(
            model_type, RESULT_GENERATOR_PROMPT, temperature, stable, more_tokens
        )

    def __repr__(self) -> str:
        return "Result Generation"

    def forward(self, data: Dict[str, str]):
        system_prompt = self.system_prompt + data["search_text"] + data["restriction"]
        user_input = """This is result from search engine: \n""" + data["information"]

        message = self.create_message(system_input=system_prompt, user_input=user_input)
        reply = super().get_reply(message)
        return reply.respond, reply.respond_with_message, reply.info
