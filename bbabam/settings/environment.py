from dotenv import dotenv_values
import openai


class OpenAIKeys:
    def __init__(self):
        self.OPENAI_API_KEY = dotenv_values(".env")["OPENAI_API_KEY"]

    def get_key(self):
        return self.OPENAI_API_KEY

    def init(self):
        openai.api_key = self.OPENAI_API_KEY


class KakaoKeys:
    def __init__(self):
        self.OPENAI_API_KEY = dotenv_values(".env")["KAKAO_API_KEY"]

    def get_key(self):
        return self.OPENAI_API_KEY
