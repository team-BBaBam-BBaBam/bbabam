import bbabam.modules.crawling_module.modules.tripbuilder_crawler as TB
import warnings
import time
from multiprocessing import Process, Manager

import multiprocessing as mp

warnings.filterwarnings(action="ignore")


class SocialCrawl:
    # 멀티프로세싱 사용해서 각 검색어당 50개의 블로그 글 수집, proxy_activate 하면 ip우회 기능 켜짐
    def __init__(self, proxy_activate=False):
        self.proxy_activate = proxy_activate
        self.crawler = TB.NaverCrawler(self.proxy_activate)
        self.keywords = []
        self.contents = []
        self.output = []

    def __repr__(self) -> str:
        return "Trip Builder Social Data Crawling Module"

    def get_links(self, query, num):
        # 블로그의 게시글 링크들을 가져옵니다.
        data = self.crawler.get_BlogURL(query, num)
        return data

    def get_content(self, url):
        content, _ = self.crawler.get_BlogInfo(url)
        if len(content) == 0:
            return None
        return content

    def Multi_Crawler(self, query, txt_num, processor_num):
        pool = mp.Pool(processes=processor_num)
        urls, tot_num = self.get_links(query, txt_num)
        lst = pool.map(self.get_content, urls)
        pool.close()
        pool.join()
        return lst, tot_num, urls

    def getTime(self, sec):
        sec = int(sec)
        h = sec // 3600
        m = (sec - h * 3600) // 60
        s = (sec - h * 3600) % 60
        return f"{h}h {m}m {s}s"

    def single_keyword_search(self, keyword, txt_num, output_list):
        conts = []
        cont_lst = []
        conts, tot_num, urls = self.Multi_Crawler(keyword, txt_num, int(txt_num / 2))
        for j in range(len(conts)):
            try:
                text = conts[j].replace("\u200b", "")
            except:
                text = ""
            cont_lst.append({"text": text, "link": urls[j]})

        output_list.append({"keywords": keyword, "contents": cont_lst})

    def forward(self, keywords, txt_num=20, on_print_message=None):
        self.keywords = keywords
        s = time.time()
        self.searched_context = []

        with Manager() as manager:
            output_list = manager.list()  # Shared list
            processes = []

            for keyword in self.keywords:
                p = Process(
                    target=self.single_keyword_search,
                    args=(keyword, txt_num, output_list),
                )
                p.start()
                processes.append(p)

            for p in processes:
                p.join()

            self.output = list(output_list)  # Convert back to regular list

            return self.output


class POICrawl:
    def __init__(self):
        self.crawler = TB.KakaoCrawler()
        self.keywords = []
        self.contents = []
