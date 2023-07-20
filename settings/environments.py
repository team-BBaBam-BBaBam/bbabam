from dotenv import dotenv_values

class Openai_keys:
    def __init__(self):
        self.OPENAI_API_KEY = dotenv_values(".env")["OPENAI_API_KEY"]

    def get_key(self):
        return self.OPENAI_API_KEY

class NotProvidedModelError(Exception):
    def __str__(self):
        return "잘못된 모델의 이름입니다. 올바른 모델의 이름은 gpt-3.5, gpt-4, word_embedding입니다."