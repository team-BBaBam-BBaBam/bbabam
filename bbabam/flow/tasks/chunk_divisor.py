from bbabam.flow.components.task import SingleTask, TaskStateType
from bbabam.flow.tasks.names import TaskNames, DataNames

from bbabam.modules.chunk_divisor import ChunkDivisor as ChunkDivisorModule


class ChunkDivisor(SingleTask):
    def __init__(self, chunk_size=1000, chunk_overlap=20):
        super().__init__(TaskNames.CHUNK_DIVISOR)
        self.chunk_divisor = ChunkDivisorModule()
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def run(self):
        self.update_state(TaskStateType.RUNNING, "Dividing Chunk")

        crawled_data = self.data_store.get_data(DataNames.CRAWLED_DATA)
        """
        crawled_data 데이터 형태:
        [
            {
                "keywords": "검색어",
                "contents": [
                    {
                        "link": "블로그 링크",
                        "text": "블로그 글 전문",  
                        ]
                    }
                ]
            }
        ]
        """

        result = list(
            map(
                lambda data: {
                    "keywords": data["keywords"],
                    "contents": self.chunk_divisor.divide_chunks(
                        filter(lambda x: x["text"] is not None, data["contents"]),
                        chunk_size=self.chunk_size,
                        chunk_overlap=self.chunk_overlap,
                    ),
                },
                crawled_data,
            )
        )

        """
        result 데이터 형태:
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
        """
        self.data_store.set_data(DataNames.CHUNK_DIVIDED_DATA, result)

        self.update_state(TaskStateType.FINISHED, "Dividing Chunk Finished")
