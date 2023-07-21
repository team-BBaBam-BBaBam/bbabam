import settings.openailm as lm
import re

class poi_decision_maker:
    def __init__(self):
        self.get_model_name = lm.Get_model_name()
        self.chatmodel = lm.Openai_chat_model(self.get_model_name.model_val(model = 'gpt-3.5', stable = 'yes'))
        print(self.chatmodel)
    
    def decision_making(self, keyword, user_input):
        note = """You will be given "search keyword" and "request in natural language". 
        This inputs might include the context of information user wants to know. 
        You should decide whether POI information is required for this context. 
        POI information is the detailed and static information such as address, operation time and categories of the place. 
        You should output the answer with 1 or 0, 1 is when POI information is needed and 0 is not. 
        And some notes here again. Your return has to include only integer, without any explanation. 
        """

        request_msg = [
            {"role": "system", "content": note},
            {"role": "user", "content": ("Search Keyword: " + keyword + "Request in natural language: " + user_input)}
        ]

        reply = self.chatmodel.get_reply(request_msg)['content']
        number = int(re.sub(r'[^0-9]', '', reply))

        if number:
            return True
        else:
            return False