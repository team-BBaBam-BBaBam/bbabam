import re
from bbabam.settings.errors import ChatExceptionError, WrongAccessError
from .base_model import ChatModel


KEYWORD_GENERATOR_PROMPT = """You will be provided with a 'natural language request', which indicates the information the user wants to know about. Your task is to generate a relevant and appropriate keyword that can be effectively used to search on a web search engine.
The keyword should be in Korean words and it can include proper nouns. 
The User, who provided 'natural language request', is foreigner who is planning to go on a trip in South Korea.

If the input is dealing with information about Kyongbokgung, you should make a keyword such as '경복궁'. You shouldn't ignore some words are proper nouns, it can be a very important information to focus on by users. And results should be detailed and specific for user input.

You should give keywords by list annotation with double quoutes. This is an example: ["keyword1", "keyword2", "keyword3"]

You should result in about 3 keywords to search, but you cannot give below 3 keywords while above 10 keywords.

And if you think you cannot provide the keywords because it is controversal or not related to the theme of korean travel, you should just return ["Improper Question"].
However, the theme of travel is not simply a recommendation of a place, but a broad range of everything foreigners are curious about Korea.

When you print out the answer for keyword list, You MUST print in list format. Do not say anything else. When you answer Improper Question, you should not answer the keywords and other explanation.
"""


class KeywordGenerator(ChatModel):
    def __init__(
        self,
        model_type: str = "gpt-4",
        temperature: float = 0.7,
        stable: bool = True,
        more_tokens: bool = False,
    ):
        super().__init__(
            model_type, KEYWORD_GENERATOR_PROMPT, temperature, stable, more_tokens
        )

    def __repr__(self) -> str:
        return "Web-Search Keyword Generation Module"

    def forward(self, user_input: str, keyword_num: int = 5):
        reply = super().forward(
            f"Request in natural language: {user_input}",
            get_system_prompt=lambda: self.system_prompt.replace(
                "<keyword_num>", str(keyword_num)
            ),
        )

        wlist = reply.respond[2:-2].split('", "')

        find_korean = re.findall("[ㄱ-힣]+", reply.respond)

        if wlist[0] == "Improper Question":
            raise ChatExceptionError
        elif len(find_korean) == 0:
            raise WrongAccessError

        return wlist, reply.respond_with_message, reply.info
