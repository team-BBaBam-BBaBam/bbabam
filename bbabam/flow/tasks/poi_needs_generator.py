from bbabam.flow.components.task import SingleTask, TaskStateType
from bbabam.flow.tasks.names import TaskNames, DataNames

from bbabam.models.poi_decision import PoiDecisionMaker

class POiNeedsGenerator(SingleTask):
    def __init__(self):
        super().__init__(TaskNames.POI_NEEDS_GENERATOR)
        self.poi_decision_maker = PoiDecisionMaker()
    
    def run(self):
        self.update_state(TaskStateType.RUNNING, "Deciding POI")

        user_input = self.data_store.get_data(DataNames.USER_INPUT)
        keywords = self.data_store.get_data(DataNames.SEARCH_KEYWORDS)

        # ERROR!!!! keywords는 리스트인데, poi_decision_maker.decision_making에서는 str로 받아들임
        # TODO: keywords를 리스트로 받아들이도록 수정
        poi, messages, info = self.poi_decision_maker.forward(keywords[0], user_input)

        self.data_store.set_data(DataNames.POI_NEEDS, poi)
        self.data_store.set_task_message(TaskNames.POI_NEEDS_GENERATOR, messages)
        self.data_store.set_task_info(TaskNames.POI_NEEDS_GENERATOR, info)
        
        self.update_state(TaskStateType.FINISHED, "POI Decided")