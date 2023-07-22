from settings.environments import OpenAIKeys
import settings.openailm as lm

class SimpleInputPrompter:
    def __init__(self):
        self.get_model_name = lm.GetModelName()
        self.chatmodel = lm.OpenAIChatModel(self.get_model_name.model_val(model = 'gpt-3.5', stable = 'yes'))

    def just_input(self, user_input):
        note = """
                You should provide some information about travel in South Korea. 
                Specifically, you are dealing with an foreigner traveler.
                """
        
        request_msg = [
            {"role": "system", "content": note},
            {"role": "user", "content": ("Request in natural language: " + user_input)}
        ]

        
        reply = self.chatmodel.get_reply(request_msg)['content']
        return reply