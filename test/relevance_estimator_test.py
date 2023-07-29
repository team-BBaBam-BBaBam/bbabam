if __name__ == "__main__":
    import sys
    import os
    current = os.path.dirname(os.path.realpath(__file__))
    parent = os.path.dirname(current)
    sys.path.append(parent)

from bbabam.modules.relevance_estimator import KeywordRelevance, SentenceRelevance
from bbabam.modules.chunk_divisor import ChunkDivisor
import bbabam.settings.openai_lm as lm

with open('test/blog_content1.txt', 'r', encoding='utf-8') as f:
        blog1 = f.read()

data = [
        {
            "text": "Hello, I am a sample text for testing the ChunkDivisor class.",
            "link": "https://example.com/sample1"
        },
        {
            "text": blog1,
            "link": "https://blog.naver.com/eun417911/223129682887"
        }
    ]

chunk_divisor = ChunkDivisor(isGpt3=False)
divided_texts = chunk_divisor.divide_chunks(data, chunk_size=200)

print(divided_texts[1]['chunks'])

keyword_sim = KeywordRelevance()
sentence_sim = SentenceRelevance()

print(sentence_sim.sentence_similarity('술', divided_texts[1]['chunks'][0:10]))
print(keyword_sim.word_accord_tokenized('술', divided_texts[1]['chunks']))