import settings.openailm as lm
import numpy as np

class CosineSimilarity:
    def __init__(self):
        self.embedmodel = lm.OpenAIEmbeddingModel()
        print(self.embedmodel)
    
    def get_vector(self, input):
        return self.embedmodel.get_embeddings(input)
    
    def relevance_cosine(self, vec1, vec2):
        return np.dot(vec1, vec2) / (np.norm(vec1)*np.norm(vec2))
    
    def mapping_nl(self, str1, str2):
        return self.relevance_cosine(self.get_vector(str1), self.get_vector(str2))
    
class KeywordRelevance:
    def __init__(self, keyword, corpus):
        self.cos_sim = CosineSimilarity()
        self.keyword = keyword
        self.corpus = corpus
    
    def text_search(self):
        s = 0
        for i in range(len(self.corpus)):
            s += self.cos_sim.relevance_cosine(self.keyword, self.corpus[i])
            val = s / len(self.corpus)
        return val
    
    def word_accord(self):
        for i in range(len(self.corpus)):
            if self.cos_sim.relevance_cosine(self.keyword, self.corpus[i]) == 1.0:
                return self.corpus

class SentenceRelevance:
    def __init__(self, sentence, corpus):
        self.cos_sim = CosineSimilarity()
        self.sentence = sentence
        self.corpus = corpus
    
    def sentence_similarity(self):
        return self.cos_sim(self.sentence, self.corpus)