from bbabam.flow.components.task import SingleTask, TaskStateType
from bbabam.flow.tasks.names import TaskNames, DataNames

from bbabam.models.keyword_generator import KeywordGenerator


class SearchKeywordGenerator(SingleTask):
    def __init__(self):
        super().__init__(TaskNames.SEARCH_KEYWORD_GENERATOR)
        self.keyword_generator = KeywordGenerator()

    def run(self):
        self.update_state(TaskStateType.RUNNING, "Generating Search Keywords")

        user_input = self.data_store.get_data(DataNames.USER_INPUT)
        keywords, message, info = self.keyword_generator.forward(user_input)

        self.data_store.set_data(DataNames.SEARCH_KEYWORDS, keywords)
        self.data_store.set_task_message(TaskNames.SEARCH_KEYWORD_GENERATOR, message)
        self.data_store.set_task_info(TaskNames.SEARCH_KEYWORD_GENERATOR, info)
        
        self.update_state(TaskStateType.FINISHED, "Search Keywords Generated")
