from bbabam.flow.components.task import SingleTask, TaskStateType
from bbabam.flow.tasks.names import TaskNames, DataNames

from bbabam.modules.crawling_module.crawling import SocialCrawl
from bbabam.database import save_multiple_data

class Crawler(SingleTask):
    def __init__(self, crawling_text_num=20):
        super().__init__(TaskNames.CRAWLER)
        self.crawler = SocialCrawl()
        self.crawling_text_num = crawling_text_num

    def run(self):
        self.update_state(TaskStateType.RUNNING, "Crawling")

        search_keywords = self.data_store.get_data(DataNames.SEARCH_KEYWORDS)

        def on_progress(message):
            self.update_state(TaskStateType.RUNNING, message)

        crawled_data = self.crawler.forward(
            search_keywords, txt_num=self.crawling_text_num, on_print_message=on_progress
        )

        for data in crawled_data:
            save_multiple_data(data["keywords"], data["contents"])

        self.data_store.set_data(DataNames.CRAWLED_DATA, crawled_data)

        self.update_state(TaskStateType.FINISHED, "Crawling Finished")
