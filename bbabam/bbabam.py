import bbabam.flow.bbabam_flow as bbabam_flow
from bbabam.flow.components.task import MultiTaskState, DefaultTaskState, TaskStateType
from bbabam.flow.tasks.names import DataNames
from bbabam.flow.components.task_data_store import TaskDataStore

import threading

from colorama import Fore, Style


def on_state_changed(state: MultiTaskState):
    import os

    def print_default_state(state: DefaultTaskState, depth: int, last=False):
        indent = "│   " * (depth - 1)
        if last:
            prefix = "└── "
        else:
            prefix = "├── "
        print(
            f"{Fore.GREEN}{indent}{prefix}{Fore.MAGENTA}[{state.task_name}]{Style.RESET_ALL}"
        )
        state_color = (
            Fore.GREEN
            if state.state == TaskStateType.FINISHED
            else Fore.YELLOW
            if state.state == TaskStateType.RUNNING
            else Fore.RED
        )
        print(
            f"{Fore.GREEN}{indent}│     {Fore.WHITE}{state.message} {state_color}({state.state}){Style.RESET_ALL}"
        )

    def print_multi_state(state: MultiTaskState, depth: int):
        indent = "│   " * (depth - 1) + "└── " if depth > 0 else ""
        print(
            f"{Fore.GREEN}{indent}[{state.task_name}] {len(state.states)} tasks{Style.RESET_ALL}"
        )
        for i, child_state in enumerate(state.states):
            last = i == len(state.states) - 1
            if child_state.type == "default":
                print_default_state(child_state, depth + 1, last)
            elif child_state.type == "multi":
                print_multi_state(child_state, depth + 1)

    global lock
    lock.acquire()

    # clear console
    os.system("cls" if os.name == "nt" else "clear")

    print("\n\nOn_state_changed: ")
    print_multi_state(state, 0)

    lock.release()


def run_bbabam(user_input: str):
    global lock
    lock = threading.Lock()

    data_store: TaskDataStore = bbabam_flow.start_flow(
        user_input=user_input, on_state_changed=on_state_changed
    )

    print(f"{Fore.BLUE}User Input{Fore.RESET}")
    print(data_store.get_data(DataNames.USER_INPUT))

    print(f"{Fore.BLUE}Search Keywords{Fore.RESET}")
    print(data_store.get_data(DataNames.SEARCH_KEYWORDS))

    print(f"{Fore.BLUE}Restrictions{Fore.RESET}")
    print(data_store.get_data(DataNames.RESTRICTIONS))

    print(f"{Fore.BLUE}Merged Data{Fore.RESET}")
    print(data_store.get_data(DataNames.MERGED_DATA))

    print(f"{Fore.BLUE}Links{Fore.RESET}")
    print(data_store.get_data(DataNames.LINKS))

    print(f"{Fore.BLUE}Result{Fore.RESET}")
    print(data_store.get_data(DataNames.RESULT))
