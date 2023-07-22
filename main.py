from settings.openailm import OpenAIChatModel, OpenAIEmbeddingModel, GetModelName
from settings.environments import OpenAIKeys

openai_chat_model = OpenAIChatModel("gpt-4-0613")
openai_embedding_model = OpenAIEmbeddingModel()
get_model_name = GetModelName()

print(openai_chat_model.get_reply([
    {"role": "system", "content": """
     You should provide some information about travel in South Korea. 
     Specifically, you are dealing with an foreigner traveler.
     """},
    {"role": "user", "content": ""}
  ]))