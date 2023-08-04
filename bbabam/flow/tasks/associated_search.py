from bbabam.flow.components.task import SingleTask, TaskStateType
from bbabam.flow.tasks.names import TaskNames, DataNames

from bbabam.models.associated_search import AssoSearchGenerator

class AssociatedSearchGenerator(SingleTask):
    def __init__(self):
        super().__init__(TaskNames.ASSO_SEARCH_GENERATOR)
        self.generator = AssoSearchGenerator()

    def run(self):
        self.update_state(TaskStateType.RUNNING, "Associated Generating")

        user_input = self.data_store.get_data(DataNames.USER_INPUT)
        result = self.data_store.get_data(DataNames.RESULT)

        associated_search, messages, info = self.generator.forward(user_input, result)

        self.data_store.set_data(DataNames.ASSOCIATED_SEARCH, associated_search)
        self.data_store.set_task_message(TaskNames.ASSO_SEARCH_GENERATOR, messages)
        self.data_store.set_task_info(TaskNames.ASSO_SEARCH_GENERATOR, info)

        self.update_state(TaskStateType.FINISHED, "Associated Search Finished")
