from settings.openailm import OpenAIChatModel, OpenAIEmbeddingModel, GetModelName
from promptingmodels.poidecision import PoiDecisionMaker
from promptingmodels.keywordgenerator import KeywordGenerator
from crawlingmodels.crawling import Crawl

crawl = Crawl()

if __name__ == '__main__': # run_crawler는 multiprocessing을 사용하고 있으므로 무조건 if name main 문 안에서만 사용하여야 합니다. KeywordGenerator도 모델을 재정의하지 않기 위해서,
                            # 이곳 안에서 사용하는 것이 좋습니다.
    keywordgenerator = KeywordGenerator()
    wlist = keywordgenerator.key_gen('Is there anything interesting in Seoul?')
    print(wlist)
    context = crawl.run_crawler(wlist)
    for i in range(5):
        print(context["Contents"][i][0])
    for i in range(5):
        print(len(context['Contents'][i]))