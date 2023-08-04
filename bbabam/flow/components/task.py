from abc import ABC, abstractmethod
from typing import Union, Callable, List
from bbabam.flow.components.task_data_store import TaskDataStore


class TaskStateType:
    READY = "ready"
    RUNNING = "running"
    FINISHED = "finished"
    FAILED = "failed"


class _TaskState:
    task_id: int
    task_name: str

    def __init__(self, task_id: int, task_name: str):
        self.task_id = task_id
        self.task_name = task_name

    def __str__(self) -> str:
        return f"{self.task_id} {self.task_name}"

    @abstractmethod
    def get_state_type(self) -> str:
        pass


class DefaultTaskState(_TaskState):
    type: str = "default"
    state: str
    message: Union[str, None]

    def __init__(
        self, task_id: int, task_name: str, state: str, message: Union[str, None]
    ):
        super().__init__(task_id, task_name)
        self.state = state
        self.message = message

    def __str__(self) -> str:
        return f"{super().__str__()} {self.state} {self.message}"

    def get_state_type(self) -> str:
        return self.state


class MultiTaskState(_TaskState):
    type: str = "multi"
    states: List[Union[DefaultTaskState, "MultiTaskState"]]

    def __init__(
        self,
        task_id: int,
        task_name: str,
        states: List[Union[DefaultTaskState, "MultiTaskState"]],
    ):
        super().__init__(task_id, task_name)
        self.states = states

    def __str__(self) -> str:
        return f"{super().__str__()} {self.states}"

    def get_state_type(self) -> str:
        is_all_ready = all(
            [state.get_state_type() == TaskStateType.READY for state in self.states]
        )
        if is_all_ready:
            return TaskStateType.READY

        is_there_running = any(
            [state.get_state_type() == TaskStateType.RUNNING for state in self.states]
        )
        if is_there_running:
            return TaskStateType.RUNNING

        is_there_failed = any(
            [state.get_state_type() == TaskStateType.FAILED for state in self.states]
        )
        if is_there_failed:
            return TaskStateType.FAILED

        return TaskStateType.FINISHED

    def find_state_by_task_id(self, task_id: int) -> Union[_TaskState, None]:
        for state in self.states:
            if state.task_id == task_id:
                return state
        return None

    def find_state_by_task_name(self, task_name: str) -> Union[_TaskState, None]:
        for state in self.states:
            if state.task_name == task_name:
                return state
        return None


class _Task:
    task_state: _TaskState
    on_state_changed: Callable[[_TaskState], None]
    data_store: TaskDataStore

    def __init__(
        self,
        task_id: int,
        task_name: str,
        on_state_changed: Callable[[_TaskState], None],
        data_store: TaskDataStore,
    ):
        self.on_state_changed = on_state_changed
        self.task_state = _TaskState(task_id, task_name)
        self.data_store = data_store

    def _update_state(self, new_state: _TaskState):
        self.task_state = new_state
        self.on_state_changed(self.task_state)

    @abstractmethod
    def run(self):
        pass


class _LateInitTask(_Task):
    def __init__(self, task_name: str):
        super().__init__(-1, task_name, lambda x: None, TaskDataStore())

    def initialize_task(
        self,
        task_id: int,
        on_state_changed: Callable[[_TaskState], None],
        data_store: TaskDataStore,
    ):
        self.task_state = _TaskState(task_id, self.task_state.task_name)
        self.on_state_changed = on_state_changed
        self.data_store = data_store

    @abstractmethod
    def run(self):
        pass


class SingleTask(_LateInitTask):
    def __init__(self, task_name: str):
        super().__init__(task_name)

    def initialize_task(
        self,
        task_id: int,
        on_state_changed: Callable[[DefaultTaskState], None],
        data_store: TaskDataStore,
    ):
        super().initialize_task(task_id, on_state_changed, data_store)
        self.task_state = DefaultTaskState(
            self.task_state.task_id,
            self.task_state.task_name,
            TaskStateType.READY,
            None,
        )

    def update_state(self, state_type: str, message: str):
        self._update_state(
            DefaultTaskState(
                self.task_state.task_id, self.task_state.task_name, state_type, message
            )
        )

    @abstractmethod
    def run(self):
        pass


class MultipleTask(_LateInitTask):
    def __init__(self, task_name: str):
        super().__init__(task_name)

    def initialize_task(
        self,
        task_id: int,
        on_state_changed: Callable[[MultiTaskState], None],
        data_store: TaskDataStore,
    ):
        super().initialize_task(task_id, on_state_changed, data_store)
        self.task_state = MultiTaskState(
            self.task_state.task_id, self.task_state.task_name, []
        )

    def update_state(self, states: List[Union[DefaultTaskState, MultiTaskState]]):
        self._update_state(
            MultiTaskState(self.task_state.task_id, self.task_state.task_name, states)
        )

    @abstractmethod
    def run(self):
        pass
