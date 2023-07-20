from dotenv import dotenv_values

class Openai_keys:
    def __init__(self):
        self.OPENAI_API_KEY = dotenv_values(".env")["OPENAI_API_KEY"]

    def get_key(self):
        return self.OPENAI_API_KEY