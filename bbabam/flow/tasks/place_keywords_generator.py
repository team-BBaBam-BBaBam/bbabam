from bbabam.flow.components.task import SingleTask, TaskStateType
from bbabam.flow.tasks.names import TaskNames, DataNames

from bbabam.models.place_decision import PlaceDataExtractor

import ast


class PlaceInfoNeedsGenerator(SingleTask):
    def __init__(self):
        super().__init__(TaskNames.PLACE_KEYWORD_EXTRACTOR)
        self.poi_decision_maker = PlaceDataExtractor()

    def run(self):
        self.update_state(TaskStateType.RUNNING, "Extracting Keywords")

        user_input = self.data_store.get_data(DataNames.USER_INPUT)
        result = self.data_store.get_data(DataNames.RESULT)

        place_keywords, messages, info = self.poi_decision_maker.forward(
            user_input, result
        )

        self.data_store.set_data(
            DataNames.PLACE_KEYWORDS, ast.literal_eval(place_keywords)
        )
        self.data_store.set_task_message(TaskNames.PLACE_KEYWORD_EXTRACTOR, messages)
        self.data_store.set_task_info(TaskNames.PLACE_KEYWORD_EXTRACTOR, info)

        self.update_state(TaskStateType.FINISHED, "Extracting Finished")
