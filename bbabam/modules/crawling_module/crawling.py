import bbabam.modules.crawling_module.modules.tripbuilder_crawler as TB
import warnings
import time

import multiprocessing as mp

warnings.filterwarnings(action='ignore')

class SocialCrawl: #멀티프로세싱 사용해서 각 검색어당 50개의 블로그 글 수집, proxy_activate 하면 ip우회 기능 켜짐
  def __init__(self, proxy_activate=False):
    self.proxy_activate = proxy_activate
    self.crawler = TB.NaverCrawler(self.proxy_activate)
    self.keywords = []
    self.contents = []
    self.output = []
  
  def get_links(self, query, num): # 블로그의 게시글 링크들을 가져옵니다.
    data = self.crawler.get_BlogURL(query,num)
    return data

  def get_content(self, url):
    content,_ = self.crawler.get_BlogInfo(url)
    if len(content)==0:
      return None
    return content

  def Multi_Crawler(self, query, txt_num, processor_num):
      pool = mp.Pool(processes=processor_num)
      urls, tot_num = self.get_links(query,txt_num)
      lst = pool.map(self.get_content, urls)
      pool.close()
      pool.join()
      return lst, tot_num, urls

  def getTime(self, sec):
    sec = int(sec)
    h = sec//3600
    m = (sec-h*3600)//60
    s = (sec-h*3600)%60
    return f"{h}h {m}m {s}s"

  def run_crawler(self, keyword, txt_num=20):
    self.keywords = keyword
    s = time.time()

    self.searched_context = []

    for i in range(len(self.keywords)):
        conts = []; cont_lst = []
        conts, tot_num, urls = self.Multi_Crawler(self.keywords[i],txt_num, int(txt_num/2))
        for j in range(len(conts)):
          try:
            text = conts[j].replace("\u200b", "")
          except:
            text = ""
          cont_lst.append({'text': text, 'link': urls[j]})
        t = time.time()
        times = (t-s)*(len(self.keywords)-i-1)/(i+1)
        print(f"\r[{i+1}/{len(self.keywords)}]|"+self.keywords[i]+f"[{tot_num}] Completed...|[Remaining time:{self.getTime(times)}]",end="")
        self.searched_context = {"keywords": self.keywords[i], "Contents": cont_lst}
        self.output.append(self.searched_context)
        if self.proxy_activate:
          time.sleep(1)
        else:
          time.sleep(5)
    return self.output

class POICrawl:
  def __init__(self):
    self.crawler = TB.KakaoCrawler()
    self.keywords = []
    self.contents = []