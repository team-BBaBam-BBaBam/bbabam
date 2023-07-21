import settings.openailm as lm
import re

class KeywordGenerator:
    def __init__(self):
        self.get_model_name = lm.GetModelName()
        self.chatmodel = lm.OpenAIChatModel(self.get_model_name.model_val(model = 'gpt-4', stable = 'yes'))
        print(self.chatmodel)
    
    def key_gen(self, user_input):
        note = """You will be given 'request in natural language' which including information about user wants to know. You should generate suitable appropriate keyword that could search well. The keyword should be in Korean words and it can include proper nouns. User is foreigner who is planning to go on a trip in South Korea.

                If the input is dealing with information about Kyongbokgung, you should make a keyword such as '경복궁'. You shouldn't ignore some words are proper nouns, it can be a very important information to focus on by users.

                You should result in about 5 keywords to search, but you cannot give below 3 keywords while above 10 keywords.
                """

        request_msg = [
            {"role": "system", "content": note},
            {"role": "user", "content": ("Request in natural language: " + user_input)}
        ]

        reply = self.chatmodel.get_reply(request_msg)['content']
        return reply