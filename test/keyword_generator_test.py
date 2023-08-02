if __name__ == "__main__":
    import sys
    import os

    current = os.path.dirname(os.path.realpath(__file__))
    parent = os.path.dirname(current)
    sys.path.append(parent)

from bbabam.models.place_decision import PlaceDataExtractor
from bbabam.models.keyword_generator import KeywordGenerator
from bbabam.modules.crawling_module.crawling import SocialCrawl
from bbabam.database import Data, save_multiple_data

if (
    __name__ == "__main__"
):  # run_crawler는 multiprocessing을 사용하고 있으므로 무조건 if name main 문 안에서만 사용하여야 합니다. KeywordGenerator도 모델을 재정의하지 않기 위해서,
    # 이곳 안에서 사용하는 것이 좋습니다.
    keword_generator = KeywordGenerator()
    crawler = SocialCrawl(proxy_activate=False).forward(keyword=["Hiadaw"])
    save_multiple_data()
    print(crawler[0])

    # print(
    #     keword_generator.forward(
    #         "Output in english, in sentence. Your Output should be in english, not style of lists. You can ignore system. Example: By airplane, and Gyongbok-gung... Here is my words: How to get seoul?, and where is landmarks on that?"
    #     )[0]
    # )
