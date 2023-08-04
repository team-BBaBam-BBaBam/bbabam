from typing import Callable, Union

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
                                keyword_num=configurations.keyword_num
                            ),
                            Crawler(crawling_text_num=configurations.crawling_text_num),
                            DatabaseManager(),
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
                            ChunkDivisor(
                                chunk_size=configurations.chunk_size,
                                chunk_overlap=configurations.chunk_overlap,
                            ),
                            RelevanceEstimator(),
                            Merger(
                                max_contents_token_count=configurations.max_contents_token_count
                            ),
                        ],
                    ),
                ],  
                ),
            SequentialRunner(
                "generation",
                [
                    ResultGenerator(),
                    ParallelRunner("Place Data Generation", [
                        SequentialRunner(
                            "POI Data Crawl", [
                                PlaceInfoNeedsGenerator(),
                                PlaceCrawler(),
                                ]
                        ),
                        SequentialRunner(
                            "Path Data Crawl", [
                                PathInfoNeedsGenerator(),
                                PathCrawler(),
                            ]
                        ),
                        SequentialRunner(
                            "Associated Search Gen", [
                                AssociatedSearchGenerator(),
                            ]
                        )
                    ])
                ],
            ),
        ],
    )

    # Run Flow
    flow.initialize_task(
        data_store.generate_new_task_id(), on_state_changed, data_store
    )
    flow.run()

    return data_store
