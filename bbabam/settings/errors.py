class NotProvidedModelError(Exception):
    def __str__(self):
        return "잘못된 모델의 이름입니다. 올바른 모델의 이름은 gpt-3.5, gpt-4, word_embedding입니다."

class ChatExceptionError(Exception):
    def __str__(self):
        return "Wrong value returned by ChatGPT APIs. Try another question which is not controversal or involved with travel."
    
class WrongAccessError(Exception):
    def __str__(self):
        return "You are to accessing wrong things to ChatGPT APIs. Try another question."
    
class WrongSimilarityScoreError(Exception):
    def __str__(self):
        return 'Try score value under 1.0, or use word_accord function when your value was 1.0.'