from settings.openailm import Openai_chat_model, Openai_embedding_model, Get_model_name

openai_chat_model = Openai_chat_model("gpt-4-0613")
openai_embedding_model = Openai_embedding_model()
get_model_name = Get_model_name()

print(openai_chat_model.get_completion([
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ]))
print(openai_chat_model.get_reply([
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ]))
print(openai_embedding_model.get_embeddings("I want you. Gumayh."))
print(get_model_name.model_val("gpt-3.5", stable="stable"))