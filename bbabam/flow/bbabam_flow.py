from typing import Callable

from bbabam.flow.tasks.names import DataNames
from bbabam.flow.components.task_data_store import TaskDataStore
from bbabam.flow.components.task import MultiTaskState
from bbabam.flow.components.sequential_runner import SequentialRunner
from bbabam.flow.components.parallel_runner import ParallelRunner

from bbabam.flow.tasks.search_keyword_generator import SearchKeywordGenerator
from bbabam.flow.tasks.crawler import Crawler
from bbabam.flow.tasks.restriction_generator import RestrictionGenerator
from bbabam.flow.tasks.poi_needs_generator import POiNeedsGenerator
from bbabam.flow.tasks.chunk_divisor import ChunkDivisor 
from bbabam.flow.tasks.relevance_estimator import RelevanceEstimator

def start_flow(user_input: str, on_state_changed: Callable[[MultiTaskState], None]):
    # Construct Flow
    data_store = TaskDataStore()
    data_store.set_data(DataNames.USER_INPUT, user_input)

    flow = SequentialRunner(
        "bbabam",
        [
            ParallelRunner(
                "preprocessing",
                [
                    SequentialRunner(
                        "meterial preparation",
                        [
                            SearchKeywordGenerator(),
                            Crawler(),
                        ],
                    ),
                    RestrictionGenerator(),
                ],
            ),
            ParallelRunner(
                "analysis",
                [
                    SequentialRunner(
                        "meterial processing",
                        [
                            ChunkDivisor(),
                            RelevanceEstimator(),
                        ],
                    ),
                    POiNeedsGenerator(),
                ],  
            ),
            ParallelRunner(
                "generation",
                [

                ],
            ),
        ],
    )

    # Run Flow
    flow.initialize_task(data_store.generate_new_task_id(), on_state_changed, data_store)
    flow.run()
