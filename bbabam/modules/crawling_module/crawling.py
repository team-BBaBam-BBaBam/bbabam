import bbabam.modules.crawling_module.modules.tripbuilder_crawler as TB
import warnings
import time
import requests

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

    def forward(self, keyword, txt_num=20, on_print_message=None):
        self.keywords = keyword
        s = time.time()

        self.searched_context = []

        for i in range(len(self.keywords)):
            conts = []
            cont_lst = []
            conts, tot_num, urls = self.Multi_Crawler(
                self.keywords[i], txt_num, int(txt_num / 2)
            )
            for j in range(len(conts)):
                try:
                    text = conts[j].replace("\u200b", "")
                except:
                    text = ""
                cont_lst.append({"text": text, "link": urls[j]})
            t = time.time()
            times = (t - s) * (len(self.keywords) - i - 1) / (i + 1)
            if on_print_message is not None:
                on_print_message(
                    f"{self.keywords[i]} Completed... ({i+1}/{len(self.keywords)}) | [Remaining time:{self.getTime(times)}]"
                )
            else:
                print(
                    f"\r[{i+1}/{len(self.keywords)}]|"
                    + self.keywords[i]
                    + f"[{tot_num}] Completed...|[Remaining time:{self.getTime(times)}]",
                    end="",
                )
            self.searched_context = {"keywords": self.keywords[i], "contents": cont_lst}
            self.output.append(self.searched_context)
            if self.proxy_activate:
                time.sleep(1)
            else:
                time.sleep(5)
        return self.output


class POICrawl:
    def __init__(self):
        self.crawler = TB.KakaoCrawler()

    def getTime(self, sec):
        sec = int(sec)
        h = sec // 3600
        m = (sec - h * 3600) // 60
        s = (sec - h * 3600) % 60
        return f"{h}h {m}m {s}s"
    
    def forward(self, place, on_print_message=None):
        s = time.time()
        self.place_name_list = place[2:-2].split(', ')
        
        poi_result = []

        try:
            for i in range(len(self.place_name_list)):
                place_name, address_name, position_XY, place_url, cate_1, cate_2, phone_num = self.crawler.get_Detail(self.place_name_list[i], version=1)
                poi_result.append({'name': place_name, 'address': address_name, 'loc_X': position_XY[0], 'loc_Y': position_XY[1], 'url': place_url, 'cate1': cate_1, 'cate2': cate_2, 'callnum': phone_num})
                t = time.time()
                times = (t - s) * (len(self.place_name_list) - i - 1) / (i + 1)
                if on_print_message is not None:
                    on_print_message(
                        f"{self.place_name_list[i]} Completed... ({i+1}/{len(self.place_name_list)}) | [Remaining time:{self.getTime(times)}]"
                    )
                else:
                    print(
                        f"\r[{i+1}/{len(self.place_name_list)}]|"
                        + self.place_name_list[i]
                        + f"Completed...|[Remaining time:{self.getTime(times)}]",
                        end="",
                    )
        except:
            pass

        return poi_result
    

class PathCrawl:
    def __init__(self):
        self.GOOGLE_API_KEY = "AIzaSyApdX8yTMrYmjbec6OppmA9Cp9p1vOBL0k"
        self.crawler = TB.KakaoCrawler()

    def forward(self, pathfinding):
        s = time.time()
        self.pathfinding_list = pathfinding[2:-2].split(', ')
        pathfinding_result = []

        try:
            pathfinding_loc = []
            for i in range(len(self.pathfinding_list)):
                    position_XY = self.crawler.get_PosXY(self.pathfinding_list[i])
                    pathfinding_loc.append(position_XY)
            apiurl = f"https://maps.googleapis.com/maps/api/directions/json?origin={pathfinding_loc[0][1]},{pathfinding_loc[0][0]} \
                                &destination={pathfinding_loc[1][1]},{pathfinding_loc[1][0]}&mode=transit&key={self.GOOGLE_API_KEY}"
            jsonobj = requests.get(apiurl).json()
                
            stepslist = []
            for i in range(len(jsonobj['routes'][0]['legs'][0]['steps'])):
                    stepslist.append({"index": str(i)+" to "+str(i+1),
                                    "distance": jsonobj['routes'][0]['legs'][0]['steps'][i]['distance'],
                                    "duration": jsonobj['routes'][0]['legs'][0]['steps'][i]['duration'],
                                    "start_location": jsonobj['routes'][0]['legs'][0]['steps'][i]['start_location'],
                                    "end_location": jsonobj['routes'][0]['legs'][0]['steps'][i]['end_location'],
                                    "html_instructions": jsonobj['routes'][0]['legs'][0]['steps'][i]['html_instructions'],
                                    "travel_mode": jsonobj['routes'][0]['legs'][0]['steps'][i]['travel_mode'],
                                    "steps" if jsonobj['routes'][0]['legs'][0]['steps'][i]['travel_mode'] == 'WALKING' else "transit_details": \
                                    jsonobj['routes'][0]['legs'][0]['steps'][i]['steps'] if jsonobj['routes'][0]['legs'][0]['steps'][i]['travel_mode'] == 'WALKING' else jsonobj['routes'][0]['legs'][0]['steps'][i]['transit_details'],
                                    })

            path_parsed = {"Total distance": jsonobj['routes'][0]['legs'][0]['distance'],
                "Total duration": jsonobj['routes'][0]['legs'][0]['duration'],
                "Startpoint": {'lat': pathfinding_loc[0][1], 'lon': pathfinding_loc[0][0]},
                "Endpoint": {'lat': pathfinding_loc[1][1], 'lon': pathfinding_loc[1][0]},
                "Steps": stepslist
                }

            pathfinding_result.append(path_parsed)

        except:
            pass

        return pathfinding_result