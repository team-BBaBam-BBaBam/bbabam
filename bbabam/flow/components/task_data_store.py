from typing import Union, Dict, Any

class TaskDataObject:
    data_name: str
    data_value: Any

    def __init__(self, data_name: str, data_value: Any):
        self.data_name = data_name
        self.data_value = data_value

class TaskDataStore:
    store:Dict[str, TaskDataObject]
    task_idx:int

    def __init__(self):
        self.store = dict()
        self.task_idx = -1

    def generate_new_task_id(self) -> int:
        self.task_idx += 1
        return self.task_idx
    
    def get_data(self, data_name: str) -> Any:
        tdobj =  self.store.get(data_name, None)
        if tdobj is None:
            return None
        return tdobj.data_value
                              
    def set_data(self, data_name: str, data_value: Any):

        self.store[data_name] = TaskDataObject(data_name, data_value)

    def remove_dataobject(self, data_name: str):
        self.store.pop(data_name, None)