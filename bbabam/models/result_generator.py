import bbabam.settings.openai_lm as lm
import re
from bbabam.settings.errors import ChatExceptionError, WrongAccessError

class ResultGenerator:
    def __init__(self):
        self.get_model_name = lm.GetModelName()
        self.chatmodel = lm.OpenAIChatModel(model=self.get_model_name.model_val(model = 'gpt-3.5', stable = 'yes', more_tokens='yes'), temperature=0.2)
        print(self.chatmodel)
    
    def result_gen(self, user_input_chat : list, restriction_chat : list, information : str):
        note = """
            Now, you should output overall conclusion according to previous chat.
            Tell me proper information considering previous chat such as my first input, and keyword and restriction you generated, and the result of searched social data.
            Tell me in language when I firstly input my request that I wanted to know.
            Use searched(given) information rather than your pre-trained insight.
            You should combine overall informations given, and answer it in 400 letters.

            Moreover, tell me the source of your inference by NAVER blog urls.


        """ + user_input_chat + restriction_chat

        input = """This is result from search engine: \n"""+information

        request_msg = [
            {"role": "system", "content": note},
        ] + [{"role": "user", "content": input}]

        reply = self.chatmodel.get_reply(request_msg)['content']
        return reply