from settings.openailm import Openai_chat_model, Openai_embedding_model, Get_model_name
from promptingmodels.poidecision import poi_decision_maker

openai_chat_model = Openai_chat_model("gpt-3.5-turbo-0613")
openai_embedding_model = Openai_embedding_model()
get_model_name = Get_model_name()
poi_decide = poi_decision_maker()

print(openai_chat_model.get_completion([
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ]))
print(openai_chat_model.get_reply([
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ]))
# print(openai_embedding_model.get_embeddings("I want you. Gumayh."))
# print(get_model_name.model_val("gpt-3.5", stable="stable"))

print(poi_decide.decision_making('Local landmarks in korea', 'I want to know local landmarks in Korea good to travel.'))
print(poi_decide.decision_making('Korean tip culture', 'Is there also tip culture in South Korea?'))
print(poi_decide.decision_making('Gang-dong-gu Pub', 'Tomorrow late night I will visit gang-dong-gu, Seoul. Is there any pub which is open also at night?'))