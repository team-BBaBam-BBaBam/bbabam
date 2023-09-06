from typing import Callable, Union
from functools import partial
import ast

from bbabam.flow.tasks.names import DataNames
from bbabam.flow.components.task_data_store import TaskDataStore
from bbabam.flow.components.task import MultiTaskState
from bbabam.flow.components.sequential_runner import SequentialRunner
from bbabam.flow.components.parallel_runner import ParallelRunner

from bbabam.flow.tasks.search_keyword_generator import SearchKeywordGenerator
from bbabam.flow.tasks.crawler import Crawler
from bbabam.flow.tasks.restriction_generator import RestrictionGenerator
from bbabam.flow.tasks.place_keywords_generator import PlaceInfoNeedsGenerator
from bbabam.flow.tasks.path_keywords_generator import PathInfoNeedsGenerator
from bbabam.flow.tasks.chunk_divisor import ChunkDivisor
from bbabam.flow.tasks.relevance_estimator import RelevanceEstimator
from bbabam.flow.tasks.merger import Merger
from bbabam.flow.tasks.result_generator import ResultGenerator
from bbabam.flow.tasks.database import DatabaseManager
from bbabam.flow.tasks.place_crawler import PlaceCrawler
from bbabam.flow.tasks.place_crawler import PathCrawler
from bbabam.flow.tasks.associated_search import AssociatedSearchGenerator
from bbabam.flow.tasks.socket_emit import ScoketEmit, ResultSocketEmit


class FlowConfigurations:
    keyword_num = 3
    crawling_text_num = 10
    chunk_size = 4000
    chunk_overlap = 50
    max_contents_token_count = 12000


def start_flow(
    user_input: str,
    on_state_changed: Callable[[MultiTaskState], None],
    configurations: Union[FlowConfigurations, None] = None,
    socket_module=None,
) -> TaskDataStore:
    # Construct Flow
    data_store = TaskDataStore()
    data_store.set_data(DataNames.USER_INPUT, user_input)

    if configurations is None:
        configurations = FlowConfigurations()

    flow = SequentialRunner(
        "bbabam",
        [
            ParallelRunner(
                "preprocessing",
                [
                    SequentialRunner(
                        "meterial preparation",
                        [
                            SearchKeywordGenerator(
                                keyword_num=configurations.keyword_num,
                            ),
                            ScoketEmit(
                                socket_module=socket_module,
                                payloads={"search_keywords": DataNames.SEARCH_KEYWORDS},
                                emit_event="start_crawling",
                            ),
                            Crawler(
                                crawling_text_num=configurations.crawling_text_num,
                            ),
                            ScoketEmit(
                                socket_module=socket_module,
                                emit_event="finish_crawling",
                            ),
                            DatabaseManager(),
                            ChunkDivisor(
                                chunk_size=configurations.chunk_size,
                                chunk_overlap=configurations.chunk_overlap,
                            ),
                            RelevanceEstimator(),
                            Merger(max_contents_token_count=configurations.max_contents_token_count),
                        ],
                    ),
                    RestrictionGenerator(),
                ],
            ),
            SequentialRunner(
                "generation",
                [
                    ResultGenerator(),
                    ResultSocketEmit(
                        socket_module=socket_module,
                        start_emit_event="start_generation",
                        end_emit_event="end_generation",
                        emit_event="generation",
                    ),
                    ParallelRunner(
                        "Place Data Generation",
                        [
                            SequentialRunner(
                                "POI Data Crawl",
                                [
                                    PlaceInfoNeedsGenerator(),
                                    PlaceCrawler(),
                                    ScoketEmit(
                                        socket_module=socket_module,
                                        payloads={
                                            "place_keywords": DataNames.SEARCHED_PLACE_KEYWORDS,
                                            "place_crawled_data": DataNames.PLACE_DATA,
                                        },
                                        emit_event="poi_generation",
                                    ),
                                ],
                            ),
                            SequentialRunner(
                                "Path Data Crawl",
                                [
                                    PathInfoNeedsGenerator(),
                                    PathCrawler(),
                                    ScoketEmit(
                                        socket_module=socket_module,
                                        payloads={
                                            "path_keywords": DataNames.PATH_KEYWORDS,
                                            "path_crawled_data": DataNames.PATHFINDING_DATA,
                                        },
                                        emit_event="path_generation",
                                    ),
                                ],
                            ),
                            SequentialRunner(
                                "Associated Search Gen",
                                [
                                    AssociatedSearchGenerator(),
                                    ScoketEmit(
                                        socket_module=socket_module,
                                        payloads={
                                            "associated_keywords": DataNames.ASSOCIATED_SEARCH,
                                        },
                                        emit_event="associated_ketwords",
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )

    # Run Flow
    flow.initialize_task(data_store.generate_new_task_id(), on_state_changed, data_store)
    flow.run()

    return data_store
