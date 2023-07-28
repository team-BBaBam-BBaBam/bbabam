from bbabam.flow.components.task import SingleTask, TaskStateType
from bbabam.flow.tasks.names import TaskNames, DataNames

from bbabam.models.restriction_information_generation import RestrictionInformationGenerator

class RestrictionGenerator(SingleTask):
    def __init__(self):
        super().__init__(TaskNames.RESTRICTION_GENERATOR)
        self.restriction_information_generator = RestrictionInformationGenerator()
    
    def run(self):
        self.update_state(TaskStateType.RUNNING, "Generating Restriction Information")

        user_input = self.data_store.get_data(DataNames.USER_INPUT)
        restriction_information = self.restriction_information_generator.generate_restriction(user_input)

        self.data_store.set_data(DataNames.RESTRICTIONS, restriction_information)
        
        self.update_state(TaskStateType.FINISHED, "Restriction Information Generated")