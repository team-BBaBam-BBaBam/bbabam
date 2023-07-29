import openai

from bbabam.settings.environments import OpenAIKeys
from bbabam.settings.errors import NotProvidedModelError

CHATGPT_3_MODEL = "gpt-3.5-turbo"
CHATGPT_3_MODEL_16K = "gpt-3.5-turbo-16k"
CHATGPT_3_MODEL_STABLE = "gpt-3.5-turbo-0613"
CHATGPT_3_MODEL_16K_STABLE = "gpt-3.5-turbo-16k-0613"
CHATGPT_4_MODEL = "gpt-4"
CHATGPT_4_MODEL_32K = "gpt-4-32k"
CHATGPT_4_MODEL_STABLE = "gpt-4-0613"
CHATGPT_4_MODEL_32K_STABLE = "gpt-4-32k-0613"
WORD_EMBEDDING_MODEL = "text-embedding-ada-002"


class OpenAIChatModel: #밑에 모델을 편하게 선택할 수 있는 get_model_name 클래스가 있지만,
                    #여기서도 바로 값을 넣어 api를 구동할 수 있음.
                    #알맞은 모델이름을 넣고 클래스 선언.
                    #함수들에 딕셔너리 형태의 메세지를 넣으면 api값을 받아옴.
                    #API 호출시 필수 파라미터가 아닌 값들은 일단 주석처리해둠.
    def __init__(self, model, functions=None, 
                 function_call=None, temperature=1.0, top_p=None, 
                 n=None, stream=None, stop=None,
                 max_tokens=None, presence_penalty=None, 
                 frequency_penalty=None, logit_bias=None, user=None):
        openai_keys = OpenAIKeys()
        openai.api_key = openai_keys.get_key()
        self.model = model
        # self.functions = functions
        # self.function_call = function_call
        self.temperature = temperature
    
        # self.top_p = top_p
        # self.n = n
        # self.stream = stream
        # self.stop = stop
        # self.max_tokens = max_tokens
        # self.presence_penalty =  presence_penalty
        # self.frequency_penalty = frequency_penalty
        # self.logit_bias = logit_bias
        # self.user = user

    def get_available(self):
        return openai.Model.list()

    def get_completion(self, messages):
        completion = openai.ChatCompletion.create(
        model=self.model,
        messages=messages,
        temperature=self.temperature
        )
        return completion
    
    def get_reply(self, messages):
        return self.get_completion(messages).choices[0].message


class OpenAIEmbeddingModel: #워드임베딩 api는 하나밖에 없으므로 모델명은 인풋으로 받지 않음.
    # 인풋문장을 넣어주면 출력되는 get_embedding 함수가 있음.
    def __init__(self):
        openai_keys = OpenAIKeys()
        openai.api_key = openai_keys.get_key()

    def get_embeddings(self, input):
        embeddings = openai.Embedding.create(
            model="text-embedding-ada-002",
            input=input
        )
        return embeddings
    
    def get_vector(self, input):
        return self.get_embeddings(input).data[0].embedding


class GetModelName: # 모델을 편하게 선택하기 위한 클래스
                    # model의 가능한 인풋은 gpt-3.5, gpt-4, word-embedding 중에 하나.
    def __init__(self):
        pass
    
    def model_val(self, model, stable=None, more_tokens=None):
            if model == 'gpt-3.5':
                if stable is not None and more_tokens is not None:
                    return CHATGPT_3_MODEL_16K_STABLE
                elif stable is not None and more_tokens is None:
                    return CHATGPT_3_MODEL_STABLE
                elif stable is None and more_tokens is not None:
                    return CHATGPT_3_MODEL_16K
                else:
                    return CHATGPT_3_MODEL
                
            elif model == 'gpt-4':
                if stable is not None and more_tokens is not None:
                    return CHATGPT_4_MODEL_32K_STABLE
                elif stable is not None and more_tokens is None:
                    return CHATGPT_4_MODEL_STABLE
                elif stable is None and more_tokens is not None:
                    return CHATGPT_4_MODEL_32K
                else:
                    return CHATGPT_4_MODEL
                
            elif model == 'word-embedding':
                return WORD_EMBEDDING_MODEL

            else:
                raise NotProvidedModelError