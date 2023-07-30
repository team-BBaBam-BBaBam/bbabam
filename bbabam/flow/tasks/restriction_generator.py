from bbabam.flow.components.task import SingleTask, TaskStateType
from bbabam.flow.tasks.names import TaskNames, DataNames

from bbabam.models.restriction_information_generation import (
    RestrictionInformationGenerator,
)


class RestrictionGenerator(SingleTask):
    def __init__(self):
        super().__init__(TaskNames.RESTRICTION_GENERATOR)
        self.restriction_information_generator = RestrictionInformationGenerator()

    def run(self):
        self.update_state(TaskStateType.RUNNING, "Generating Restriction Information")

        user_input = self.data_store.get_data(DataNames.USER_INPUT)
        restriction_information, message, info = self.restriction_information_generator.forward(
            user_input
        )

        self.data_store.set_data(DataNames.RESTRICTIONS, restriction_information)
        self.data_store.set_task_message(TaskNames.RESTRICTION_GENERATOR, message)
        self.data_store.set_task_info(TaskNames.RESTRICTION_GENERATOR, info)

        self.update_state(TaskStateType.FINISHED, "Restriction Information Generated")
