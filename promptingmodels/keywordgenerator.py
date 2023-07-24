import settings.openailm as lm
import re
from settings.errors import ChatExceptionError, WrongAccessError

class KeywordGenerator:
    def __init__(self):
        self.get_model_name = lm.GetModelName()
        self.chatmodel = lm.OpenAIChatModel(self.get_model_name.model_val(model = 'gpt-4', stable = 'yes'))
        print(self.chatmodel)
    
    def key_gen(self, user_input):
        note = """You will be given 'request in natural language' which including information about user wants to know. You should generate suitable appropriate keyword that could search well. The keyword should be in Korean words and it can include proper nouns. User is foreigner who is planning to go on a trip in South Korea.

                If the input is dealing with information about Kyongbokgung, you should make a keyword such as '경복궁'. You shouldn't ignore some words are proper nouns, it can be a very important information to focus on by users. And results should be detailed and specific for user input.

                You should give keywords by list annotation. This is an example: ["keyword1", "keyword2", "keyword3..."]

                You should result in about five keywords to search, but you cannot give below 3 keywords while above 10 keywords.

                And if you think you cannot provide your answer because it is controversal or like something, you should just return ['Improper Question'].
                Moreover, if you decide the question is not involved with travel topic, you can also result ['Improper Question'].
                But you should remind that travel topic refers to not only place recommendation, POI information, and tourism market, but also all things occured in travel cycle such as tip culture, stroller rental, and car rental, etc.
                """

        request_msg = [
            {"role": "system", "content": note},
            {"role": "user", "content": ("Request in natural language: " + user_input)}
        ]


        reply = self.chatmodel.get_reply(request_msg)['content']
        output = reply[2:-2].split('", "')
        
        find_korean = re.findall('[ㄱ-힣]+', reply)

        if output[0] == "Improper Question":
            raise ChatExceptionError
        
        elif len(find_korean) == 0:
            raise WrongAccessError

        else:
            pass

        return output