from bbabam.flow.components.task import SingleTask, TaskStateType
from bbabam.flow.tasks.names import TaskNames, DataNames

from bbabam.modules.crawling_module.crawling import POICrawl, PathCrawl

class PlaceCrawler(SingleTask):
    def __init__(self):
        super().__init__(TaskNames.PLACE_CRAWLER)
        self.crawler = POICrawl()

    def run(self):
        self.update_state(TaskStateType.RUNNING, "Place Crawling")

        place_keywords = self.data_store.get_data(DataNames.PLACE_KEYWORDS)

        def on_progress(message):
            self.update_state(TaskStateType.RUNNING, message)

        place_data = self.crawler.forward(
            place_keywords, on_print_message=on_progress
        )
        self.data_store.set_data(DataNames.PLACE_DATA, place_data)

        self.update_state(TaskStateType.FINISHED, "Place Crawling Finished")

class PathCrawler(SingleTask):
    def __init__(self):
        super().__init__(TaskNames.PATH_CRAWLER)
        self.crawler = PathCrawl()

    def run(self):
        self.update_state(TaskStateType.RUNNING, "Path Crawling")

        path_keywords = self.data_store.get_data(DataNames.PATH_KEYWORDS)

        def on_progress(message):
            self.update_state(TaskStateType.RUNNING, message)

        pathfinding_data = self.crawler.forward(
            path_keywords
        )
        self.data_store.set_data(DataNames.PATHFINDING_DATA, pathfinding_data)

        self.update_state(TaskStateType.FINISHED, "Path Crawling Finished")
