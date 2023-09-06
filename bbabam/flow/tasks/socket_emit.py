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
            self.socket_module.emit(self.emit_event, data, namespace=self.namespace, room=self.room)

    def run(self):
        self.update_state(TaskStateType.RUNNING, "Emit...")
        data = {}
        for key, value in self.payloads.items():
            data[key] = self.data_store.get_data(value)

        self.emit(data)
        self.update_state(TaskStateType.FINISHED, "Done")


class ResultSocketEmit(ScoketEmit):
    def __init__(self, socket_module, start_emit_event: str, emit_event: str, end_emit_event: str) -> None:
        super().__init__(socket_module, emit_event, {})
        self.end_emit_event = end_emit_event
        self.start_emit_event = start_emit_event

    def emit(self):
        with self.app.app_context():
            urls = self.data_store.get_data(DataNames.LINKS)
            results = self.data_store.get_data(DataNames.RESULT)
            self.socket_module.emit(self.start_emit_event, {"urls": urls}, namespace=self.namespace, room=self.room)

            result_text = ""

            for chunk in results:
                content = chunk["choices"][0].get("delta", {}).get("content")
                if content is not None:
                    result_text += content
                    self.socket_module.emit(self.emit_event, {"word": content}, namespace=self.namespace, room=self.room)

            self.data_store.set_data(DataNames.RESULT, result_text)
            self.socket_module.emit(self.end_emit_event, {}, namespace=self.namespace, room=self.room)

    def run(self):
        self.update_state(TaskStateType.RUNNING, "Emit...")
        self.emit()
        self.update_state(TaskStateType.FINISHED, "Done")
