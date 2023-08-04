from typing import Dict
from flask import Flask
from bbabam.flow.components.task import SingleTask, TaskStateType
from bbabam.flow.tasks.names import TaskNames, DataNames


class ScoketEmit(SingleTask):
    def __init__(
        self,
        socket_module,
        emit_event: str,
        payloads: Dict = {},
    ) -> None:
        super().__init__(TaskNames.SOCKETIO_EMIT)

        self.app = socket_module["app"]
        self.socket_module = socket_module["emit"]
        self.namespace = socket_module["namespace"]
        self.room = socket_module["room"]
        self.emit_event = emit_event
        self.payloads = payloads if isinstance(payloads, dict) else payloads()

    def emit(self, data: Dict):
        with self.app.app_context():
            print(data, self.room, self.namespace)
            self.socket_module.emit(
                self.emit_event, data, namespace=self.namespace, room=self.room
            )

    def run(self):
        self.update_state(TaskStateType.RUNNING, "Emit...")
        data = {}
        for key, value in self.payloads.items():
            data[key] = self.data_store.get_data(value)

        self.emit(data)
        self.update_state(TaskStateType.FINISHED, "Done")
