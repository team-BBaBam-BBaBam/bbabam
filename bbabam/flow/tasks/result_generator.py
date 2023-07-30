from bbabam.flow.components.task import SingleTask, TaskStateType
from bbabam.flow.tasks.names import TaskNames, DataNames

from bbabam.models.result_generator import ResultGenerator as ResultGeneratorModule


class ResultGenerator(SingleTask):
    def __init__(self):
        super().__init__(TaskNames.RESULT_GENERATOR)
        self.result_generator = ResultGeneratorModule()

    def run(self):
        self.update_state(TaskStateType.RUNNING, "Generating Result")

        user_input = self.data_store.get_data(DataNames.USER_INPUT)
        restrictions = self.data_store.get_data(DataNames.RESTRICTIONS)
        information = self.data_store.get_data(DataNames.MERGED_DATA)

        respond, respond_with_message, info = self.result_generator.forward(
            user_input, restrictions, information
        )

        self.data_store.set_data(DataNames.RESULT, respond)
        self.data_store.set_task_message(
            TaskNames.RESULT_GENERATOR, respond_with_message
        )
        self.data_store.set_task_info(TaskNames.RESULT_GENERATOR, info)

        self.update_state(TaskStateType.FINISHED, "Result Generated")
