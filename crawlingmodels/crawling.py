import Modules.TripBuilder as TB
import warnings
import time

import Modules.TripBuilder as TB
from multiprocessing import Pool

warnings.filterwarnings(action='ignore')

crawler = TB.NaverCrawler()

def get_links(query,num): # 블로그의 게시글 링크들을 가져옵니다.
    data = crawler.get_BlogURL(query,num)
    return data

def get_content(url):
    content,_ = crawler.get_BlogInfo(url)
    if len(content)==0:
      return None
    return content

def Multi_Crawler(query,num):
    pool = Pool(processes=10)
    urls, tot_num = get_links(query,num)
    lst = pool.map(get_content, urls)
    return lst, tot_num

def getTime(sec):
  sec = int(sec)
  h = sec//3600
  m = (sec-h*3600)//60
  s = (sec-h*3600)%60
  return f"{h}h {m}m {s}s"

# PLA000 Version 추출 -> 후가공
# 일 최대 10만개 / 월 최대 300만개 장소 데이터 수집 가능(poi 이슈로 인해)

crawler = TB.NaverCrawler()
poi_crawler = TB.KakaoCrawler()

name = []; ids = []
cate1 = []; cate2 = []
locX = []; locY = []
address = []; callnum = []
op_time = []; restday = []
contents = []; imgs = []
tag = []; num_txt = []
spend_avg = []; fee = []
dem_info = []; staytime = []
visit = []; bus_code = []
filter = []; cong = []

s = time.time()
id_num = 0

for i in range(len(place)):
  conts = []; cont_lst = []

  p_info = place["주소"][i].split()
  B_city = p_info[0].strip("특별시").strip("광역시").strip("특별자치도")
  s_city = p_info[1]
  p_info = B_city#" ".join([B_city,s_city])

  place_name = p_info+" "+place["장소명"][i]
  try:
    conts, tot_num = Multi_Crawler(place_name,40)
    for cont in conts:
      if(cont!=None):
        cont_lst.append(cont)
    """
    position_XY, place_url, cate_1, cate_2, phone_num = poi_crawler.get_Detail(place_name, version=1)

    if len(str(phone_num))==3:
      pass #phone_num = place["telNo"][i]

    if np.isnan(float(position_XY[0])):
      if place['lon'][i]<place['lat'][i]:
        place['lon'][i],place['lat'][i] = place['lat'][i],place['lon'][i]

      position_XY = [place['lon'][i],place['lat'][i]]

    try:
      if np.isnan(cate_1):
        cate_1 = place['큰카테고리'][i].split(">")[0]
        if cate_1 == "카페/디저트":
          cate_1 = "카페"
        elif cate_1 in ["맛집","음식점"]:
          cate_1 = "음식점"
        cate_2 = place['큰카테고리'][i].split(">")[-1]
    except:
      pass

    optime = [place["startTime"][i],place["endTime"][i]]
    """

    name.append(place["장소명"][i])
    """
    ids.append(id_num); id_num+=1
    cate1.append(cate_1)
    cate2.append(cate_2)
    locX.append(position_XY[0])
    locY.append(position_XY[1])
    address.append(place["주소"][i])
    callnum.append(phone_num)
    op_time.append(optime)
    restday.append(np.nan)
    """
    contents.append(cont_lst)
    """
    imgs.append(np.nan)
    tag.append(np.nan)
    num_txt.append(tot_num)
    spend_avg.append(np.nan)
    fee.append(np.nan)
    dem_info.append(np.nan)
    staytime.append(np.nan)
    visit.append(np.nan)
    bus_code.append(np.nan)
    filter.append(np.nan)
    cong.append(np.nan)
    """

    t = time.time()
    times = (t-s)*(len(place)-i-1)/(i+1)
    print(f"\r[{i+1}/{len(place)}]|"+place["장소명"][i]+f"[{tot_num}] Completed...|[Remaining time:{getTime(times)}]",end="")

  except:
    pass

# data_path = "/content/drive/MyDrive/tripbuilder_data/"
# tot_df.to_json(data_path+f"Ulsan_smart_final_PLA000_4.json")