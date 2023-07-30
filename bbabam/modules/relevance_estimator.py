import tiktoken
import numpy as np
from numpy.linalg import norm
import re
from bbabam.models.base_model import OpenAIEmbeddingModel 


def list_compare(target, source):
    targetchar = "".join(str(word) for word in target)
    sourcechar = "".join(str(word) for word in source)
    location_list = []
    for i in range(len(source)):
        if sourcechar[: len(targetchar)] == targetchar:
            location_list.append(i)
        sourcechar = sourcechar[len(str(source[i])) :]
    return location_list


class CosineSimilarity:
    def __init__(self):
        self.embedmodel = OpenAIEmbeddingModel()

    def get_vector(self, input):
        return self.embedmodel.get_vector(input)

    def relevance_cosine(self, vec1, vec2):
        return np.dot(vec1, vec2) / (norm(vec1) * norm(vec2))

    def mapping_nl(self, str1, str2):
        return self.relevance_cosine(self.get_vector(str1), self.get_vector(str2))


class KeywordRelevance:
    def __init__(self):
        self.cos_sim = CosineSimilarity()

    def keyword_similarity(self, keyword, chunks):
        sim_info = []
        for i in range(len(chunks)):
            val = self.cos_sim.mapping_nl(keyword, chunks[i]["text"])
            sim_info.append(
                {
                    "chunk_num": i,
                    "chunks": chunks[i],
                    "keyword": keyword,
                    "similarity": val,
                }
            )
        return sim_info

    def word_accord(self, keyword, chunks, around_w=10):
        accords_info = []
        for i in range(len(chunks)):
            words = chunks[i]["text"]
            loc = []
            for text in re.finditer(keyword, words):
                loc.append(text.start())
            for index in loc:
                accords_info.append(
                    {
                        "chunk_num": i,
                        "chunks": chunks[i],
                        "keyword": keyword,
                        "word_around": words[
                            max(0, index - around_w) : min(len(words), index + around_w)
                        ],
                    }
                )

        return accords_info

    def word_accord_tokenized(self, keyword, chunks, around_w=10):
        accords_info = []
        enc = tiktoken.encoding_for_model("gpt-4")
        for i in range(len(chunks)):
            words = enc.encode(chunks[i]["text"])
            for index in list_compare(enc.encode(keyword), words):
                print(index)
                print(len(words))
                accords_info.append(
                    {
                        "chunk_num": i,
                        "chunks": chunks[i],
                        "keyword": keyword,
                        "word_around": enc.decode(
                            words[
                                max(0, index - around_w) : min(
                                    len(words), index + around_w
                                )
                            ]
                        ),
                    }
                )
        return accords_info


class SentenceRelevance:
    def __init__(self):
        self.cos_sim = CosineSimilarity()

    def sentence_similarity(self, sentence, chunks):
        sim_info = []
        for i in range(len(chunks)):
            val = self.cos_sim.mapping_nl(sentence, chunks[i]["text"])
            sim_info.append(
                {
                    "chunk_num": i,
                    "chunks": chunks[i],
                    "sentence": sentence,
                    "similarity": val,
                }
            )
        return sim_info
