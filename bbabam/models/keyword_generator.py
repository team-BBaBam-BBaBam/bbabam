import re
from bbabam.settings.errors import ChatExceptionError, WrongAccessError
from .base_model import OpenAIChatModel


KEYWORD_GENERATOR_PROMPT = """You will be given 'request in natural language' which including information about user wants to know. You should generate suitable appropriate keyword that could search well. The keyword should be in Korean words and it can include proper nouns. User is foreigner who is planning to go on a trip in South Korea.

If the input is dealing with information about Kyongbokgung, you should make a keyword such as '경복궁'. You shouldn't ignore some words are proper nouns, it can be a very important information to focus on by users. And results should be detailed and specific for user input.

You should give keywords by list annotation. This is an example: ["keyword1", "keyword2", "keyword3..."]

You should result in about five keywords to search, but you cannot give below 3 keywords while above 10 keywords.

And if you think you cannot provide your answer because it is controversal or like something, you should just return ['Improper Question'].
Moreover, if you decide the question is not involved with travel topic, you can also result ['Improper Question'].
But you should remind that travel topic refers to not only place recommendation, POI information, and tourism market, but also all things occured in travel cycle such as tip culture, stroller rental, and car rental, etc.
"""


class KeywordGenerator(OpenAIChatModel):
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

    def forward(self, user_input: str):
        reply = super().forward(f"Request in natural language: {user_input}")
        wlist = reply.respond[2:-2].split('", "')

        find_korean = re.findall("[ㄱ-힣]+", reply.respond)

        if wlist[0] == "Improper Question":
            raise ChatExceptionError
        elif len(find_korean) == 0:
            raise WrongAccessError

        return wlist, reply.respond_with_message, reply.info
