import bbabam.models as models
import bbabam.modules as modules
import time
import json

class TimeCheker():
    def __init__(self) -> None:
        self.__s_time = None
        self.__e_time = None

    def __clear(self):
        self.__s_time = None
        self.__e_time = None

    def start(self):
        self.__s_time = time.time()
        
    def end(self):
        self.__e_time = time.time()
        print()
        print("Time Elapsed: " + str(self.__e_time - self.__s_time), "seconds")
        print()
        
        self.__clear()

class Agent:
    def __init__(self) -> None:
        self.keywords_generator = models.KeywordGenerator()
        self.poi_decision = models.PoiDecisionMaker()
        self.restriction_generator = models.RestrictionInformationGenerator()
        self.result_generator = models.ResultGenerator()

        self.chunk_divisor = modules.ChunkDivisor()
        self.crawler = modules.SocialCrawl()

        self.chat_history = []
    
    def log(self, text):
        print("-" * 10, text, "-" * 10)

    def call(self):
        st = time.time()
        time_checker = TimeCheker()
        search_text = input("Input Text : ")
        # search_text = "How many Starbucks are there in Daejeon Shinsegae Department Store?"
        time_checker.start()
        self.log("Web-Search Keyword Generation Module")
        wlist, hist = self.keywords_generator.key_gen(search_text)
        self.chat_history.append(hist)
        time_checker.end()
        print(wlist)

        time_checker.start()
        self.log("Trip Builder Social Data Crawling Module")
        context = self.crawler.run_crawler(wlist[:2])
        context = [content['Contents'][:3] for content in context]
        time_checker.end()
        print(str(context)[:300])


        time_checker.start()
        self.log("Restriction information Generation Module")
        restriction, hist = self.restriction_generator.generate_restriction(search_text)
        self.chat_history.append(hist)
        time_checker.end()
        print(restriction)


        time_checker.start()
        self.log("Result Generation")
        output = self.result_generator.result_gen(search_text, restriction, str(context))
        time_checker.end()

        print(output)
        et = time.time()
        print("Total :",et - st, "seconds")

        print(111)


if __name__ == "__main__":
    agent = Agent()
    agent.call()