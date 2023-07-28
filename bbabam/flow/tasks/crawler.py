from bbabam.flow.components.task import SingleTask, TaskStateType
from bbabam.flow.tasks.names import TaskNames, DataNames

from bbabam.modules.crawling_module.crawling import SocialCrawl

class Crawler(SingleTask):
    def __init__(self):
        super().__init__(TaskNames.CRAWLER)
        self.crawler = SocialCrawl()
    
    def run(self):
        self.update_state(TaskStateType.RUNNING, "Crawling")

        search_keywords = self.data_store.get_data(DataNames.SEARCH_KEYWORDS)
        def on_progress(message):
            self.update_state(TaskStateType.RUNNING, message)
        crawled_data = self.crawler.run_crawler(search_keywords, on_progress)
        self.data_store.set_data(DataNames.CRAWLED_DATA, crawled_data)

        self.update_state(TaskStateType.FINISHED, "Crawling Finished")