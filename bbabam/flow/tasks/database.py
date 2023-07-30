from bbabam.flow.components.task import SingleTask, TaskStateType
from bbabam.flow.tasks.names import TaskNames, DataNames

from bbabam.database import save_multiple_data


class DatabaseManager(SingleTask):
    def __init__(self):
        super().__init__(TaskNames.INSERT_TO_DATABASE)

    def run(self):
        self.update_state(TaskStateType.RUNNING, "Inserting to Database")

        user_input = self.data_store.get_data(DataNames.USER_INPUT)
        crawled_data = self.data_store.get_data(DataNames.CRAWLED_DATA)

        for data in crawled_data:
            save_multiple_data(
                keyword=data["keywords"],
                user_input=user_input,
                data_list=data["contents"],
            )

        self.update_state(TaskStateType.FINISHED, "Inserted")
