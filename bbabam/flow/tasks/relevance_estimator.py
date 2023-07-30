from typing import Callable
from bbabam.flow.components.task import DefaultTaskState, MultiTaskState,SingleTask, TaskStateType
from bbabam.flow.components.parallel_runner import ParallelRunner
from bbabam.flow.components.task_data_store import TaskDataStore
from bbabam.flow.tasks.names import TaskNames, DataNames

from bbabam.modules.relevance_estimator import KeywordRelevance, SentenceRelevance

class _SingleRelavanceEstimator(SingleTask):
    def __init__(self, index:int, user_input: str, keywords: str, contents: list):
        super().__init__(TaskNames.RELEVANCE_ESTIMATOR_SUBTASK)
        self.index = index
        self.user_input = user_input
        self.keywords = keywords
        self.contents = contents

    def run(self):
        self.update_state(TaskStateType.RUNNING, "Estimating Relevance")

        keyword_relevance = KeywordRelevance()
        # sentence_relevance = SentenceRelevance()

        keyword_sim_info = keyword_relevance.keyword_similarity(self.keywords, self.contents)
        # sentence_sim_info = sentence_relevance.sentence_similarity(self.user_input, self.contents)

        self.data_store.set_data(f"relevance{self.index}", map(lambda info: info["similarity"],keyword_sim_info))
        self.update_state(TaskStateType.FINISHED, "Estimating Relevance Finished")


class _ParallelRelevanceEstimator(ParallelRunner):
    def __init__(self):
        super().__init__(TaskNames.RELEVANCE_ESTIMATOR, [])

    def run(self):
        divided_chunk = self.data_store.get_data(DataNames.CHUNK_DIVIDED_DATA)
        '''
        divided_chunk 데이터 형태:
        [
            {
                "keywords": "검색어",
                "contents": [
                    {
                        "link": "블로그 링크",
                        "total_token_count": 1234,
                        "chunks": [
                            {
                                "text": "블로그 글 첫번째 청크",
                                "token_count": 123
                            }
                        ]
                    }
                ]
            }
        ]
        '''
        user_input = self.data_store.get_data(DataNames.USER_INPUT)
        flattened_data = []
        for data in divided_chunk:
            for content in data["contents"]:
                flattened_data.append({
                    "keywords": data["keywords"],
                    "link": content["link"],
                    "total_token_count": content["total_token_count"],
                    "chunks": content["chunks"]
                })
        '''
        flattened_data 데이터 형태:
        [
            {
                "keywords": "검색어",
                "link": "블로그 링크",
                "total_token_count": 1234,
                "chunks": [
                    {
                        "text": "블로그 글 첫번째 청크",
                        "token_count": 123
                    }
                ]
            }
        ]
        '''
        # Add Relevance Estimator Tasks
        for index, data in enumerate(flattened_data):
            self.add_task(_SingleRelavanceEstimator(index, user_input, data["keywords"], data["chunks"]))
            
        super().run()

        for index in range(len(flattened_data)):
            data = self.data_store.get_data(f"relevance{index}")
            for i, sim in enumerate(data):
                flattened_data[index]["chunks"][i]["similarity"] = sim
            self.data_store.remove_data(f"relevance{index}")

        self.data_store.set_data(DataNames.RELEVANCE_DATA, flattened_data)
        '''
        flattened_data 데이터 형태:
        [
            {
                "keywords": "검색어",
                "link": "블로그 링크",
                "total_token_count": 1234,
                "chunks": [
                    {
                        "text": "블로그 글 첫번째 청크",
                        "similarity": 0.123,
                        "token_count": 123
                    }
                ]
            }
        ]
        '''

class RelevanceEstimator(SingleTask):
    def __init__(self):
        super().__init__(TaskNames.RELEVANCE_ESTIMATOR)
        self.parallel_relevance_estimator = _ParallelRelevanceEstimator()

    def initialize_task(self, task_id: int, on_state_changed: Callable[[DefaultTaskState], None], data_store: TaskDataStore):
        super().initialize_task(task_id, on_state_changed, data_store)
        self.parallel_relevance_estimator.initialize_task(data_store.generate_new_task_id(), self._on_state_change, data_store)

    def _on_state_change(self, state: MultiTaskState):
        # count finished tasks
        finished_count = 0
        for child_state in state.states:
            if child_state.state == TaskStateType.FINISHED:
                finished_count += 1
        
        if self.task_state.state == TaskStateType.READY:
            return

        if finished_count == len(state.states) and len(state.states) > 0:
            self.update_state(TaskStateType.FINISHED, f"Estimating Relevance Finished ({finished_count}/{len(state.states)})")
        else:
            self.update_state(TaskStateType.RUNNING, f"Estimating Relevance ({finished_count}/{len(state.states)})")
        

    def run(self):
        self.update_state(TaskStateType.RUNNING, "Estimating Relevance")

        self.parallel_relevance_estimator.run()