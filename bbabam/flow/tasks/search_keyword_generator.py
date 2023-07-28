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
        keywords = self.keyword_generator.key_gen(user_input)

        self.data_store.set_data(DataNames.SEARCH_KEYWORDS, keywords)

        self.update_state(TaskStateType.FINISHED, "Search Keywords Generated")
        