from typing import Dict, Any, List

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

    def set_task_message(self, task_name:str, message:List[Dict[str, str]]):
        self.set_data(f"{task_name}_message", message)
    
    def get_task_message(self, task_name:str) -> List[Dict[str, str]]:
        return self.get_data(f"{task_name}_message")
    
    def set_task_info(self, task_name:str, info:Dict[str, Any]):
        self.set_data(f"{task_name}_info", info)

    def get_task_info(self, task_name:str) -> Dict[str, Any]:
        return self.get_data(f"{task_name}_info")
    
    def remove_data(self, data_name: str):
        self.store.pop(data_name, None)