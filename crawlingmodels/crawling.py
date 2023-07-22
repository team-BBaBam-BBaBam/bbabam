import crawlingmodels.Modules.TripBuilderCrawler as TB
import warnings
import time

import multiprocessing as mp

warnings.filterwarnings(action='ignore')

class Crawl: #멀티프로세싱 사용해서 각 검색어당 50개의 블로그 글 수집
  def __init__(self):
    self.crawler = TB.NaverCrawler()
    self.poi_crawler = TB.KakaoCrawler()
    self.keywords = []
    self.contents = []
  
  def get_links(self, query, num): # 블로그의 게시글 링크들을 가져옵니다.
    data = self.crawler.get_BlogURL(query,num)
    return data

  def get_content(self, url):
    content,_ = self.crawler.get_BlogInfo(url)
    if len(content)==0:
      return None
    return content

  def Multi_Crawler(self, query,num):
      pool = mp.Pool(processes=10)
      urls, tot_num = self.get_links(query,num)
      lst = pool.map(self.get_content, urls)
      pool.close()
      pool.join()
      return lst, tot_num

  def getTime(self, sec):
    sec = int(sec)
    h = sec//3600
    m = (sec-h*3600)//60
    s = (sec-h*3600)%60
    return f"{h}h {m}m {s}s"

  def run_crawler(self, keyword):
    self.keywords = keyword
    s = time.time()

    for i in range(len(self.keywords)):
      #try:
        conts = []; cont_lst = []
        conts, tot_num = self.Multi_Crawler(self.keywords[i],50)
        for cont in conts:
          if(cont!=None):
            cont_lst.append(cont)
        self.contents.append(cont_lst)
        t = time.time()
        times = (t-s)*(len(self.keywords)-i-1)/(i+1)
        print(f"\r[{i+1}/{len(self.keywords)}]|"+self.keywords[i]+f"[{tot_num}] Completed...|[Remaining time:{self.getTime(times)}]",end="")
      #except:
      #  pass
        time.sleep(1)
    return {"Keywords": self.keywords, "Contents": self.contents}