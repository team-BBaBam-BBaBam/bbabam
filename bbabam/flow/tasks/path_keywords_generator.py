from bbabam.flow.components.task import SingleTask, TaskStateType
from bbabam.flow.tasks.names import TaskNames, DataNames

from bbabam.models.path_decision import PathDataExtractor

class PathInfoNeedsGenerator(SingleTask):
    def __init__(self):
        super().__init__(TaskNames.PATH_KEYWORD_EXTRACTOR)
        self.path_decision_maker = PathDataExtractor()
    
    def run(self):
        self.update_state(TaskStateType.RUNNING, "Extracting Keywords")

        user_input = self.data_store.get_data(DataNames.USER_INPUT)
        result = self.data_store.get_data(DataNames.RESULT)

        path_keywords, messages, info = self.path_decision_maker.forward(user_input, result)

        self.data_store.set_data(DataNames.PATH_KEYWORDS, path_keywords)
        self.data_store.set_task_message(TaskNames.PATH_KEYWORD_EXTRACTOR, messages)
        self.data_store.set_task_info(TaskNames.PATH_KEYWORD_EXTRACTOR, info)
        
        self.update_state(TaskStateType.FINISHED, "Extracting Finished")