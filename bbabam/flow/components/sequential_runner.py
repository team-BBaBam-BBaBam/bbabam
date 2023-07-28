from typing import List, Union, Callable
from bbabam.flow.components.task_data_store import TaskDataStore
from bbabam.flow.components.task import MultipleTask, SingleTask, MultiTaskState, DefaultTaskState


class SequentialRunner(MultipleTask):
    tasks: List[Union[SingleTask, MultipleTask]]

    def __init__(self, task_name: str, tasks: List[Union[SingleTask, MultipleTask]]):
        super().__init__(task_name)
        self.tasks = tasks

    def initialize_task(self, task_id: int, on_state_changed: Callable[[MultiTaskState], None], data_store: TaskDataStore):
        super().initialize_task(task_id, on_state_changed, data_store)
        self.initialize_child_tasks()
    
    def initialize_child_tasks(self):
        def on_task_state_changed(task_state: Union[MultiTaskState, DefaultTaskState]):
            self._on_task_state_changed(task_state)
        
        for task in self.tasks:
            task.initialize_task(self.data_store.generate_new_task_id(), on_task_state_changed, self.data_store)
        
        task_states = list(map(lambda task: task.task_state, self.tasks))
        self.update_state(task_states)
    
    def _on_task_state_changed(self, task_state: Union[MultiTaskState, DefaultTaskState]):
        # Update state
        self.update_state(
            list(map(
                lambda state: state if not task_state.task_id == state.task_id else task_state,  self.task_state.states
            ))
        )

    def run(self):
        # Start all Single Tasks
        for task in self.tasks:
            task.run()