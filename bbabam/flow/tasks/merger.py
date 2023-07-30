from bbabam.flow.components.task import SingleTask, TaskStateType
from bbabam.flow.tasks.names import TaskNames, DataNames


class Merger(SingleTask):
    def __init__(self, max_contents_token_count=3000):
        super().__init__(TaskNames.MERGER)
        self.max_contents_token_count = max_contents_token_count

    def run(self):
        self.update_state(TaskStateType.RUNNING, "Merging")

        chunk_divided_data = self.data_store.get_data(DataNames.RELEVANCE_DATA)
        """
        chunk_divided_data 데이터 형태:
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
        """

        sorted_data = []
        # flatten
        for data in chunk_divided_data:
            for chunk in data["chunks"]:
                sorted_data.append(
                    {
                        "link": data["link"],
                        "keywords": data["keywords"],
                        "chunk_text": chunk["text"],
                        "similarity": chunk["similarity"],
                        "token_count": chunk["token_count"],
                    }
                )
        # sort
        sorted_data.sort(key=lambda data: data["similarity"], reverse=True)
        """
        sorted_data 데이터 형태:
        [
            {
                "link": "블로그 링크",
                "keywords": "검색어",
                "chunk_text": "블로그 글 첫번째 청크",
                "similarity": 0.123,
                "token_count": 123
            }
        ]
        """

        # get top k data
        max_token_count = self.max_contents_token_count
        picked_data = []
        token_count = 0
        for data in sorted_data:
            if token_count + data["token_count"] > max_token_count:
                break
            picked_data.append(data)
            token_count += data["token_count"]

        # 같은 링크의 청크들을 하나로 합침
        merged_data = {}
        for data in picked_data:
            if data["link"] not in merged_data:
                merged_data[data["link"]] = [
                    {
                        "link": data["link"],
                        "keywords": data["keywords"],
                        "text": data["chunk_text"],
                    }
                ]
            else:
                merged_data[data["link"]].append(
                    {
                        "link": data["link"],
                        "keywords": data["keywords"],
                        "text": data["chunk_text"],
                    }
                )

        # plain text로 만들기
        # 규칙
        # [link 1/5 start] \n https://... \n [chunk 1/2 start] \n [chunk 1/2 end] \n [chunk 2/2 start] \n [chunk 2/2 end] \n [link 1/5 end] \n
        merged_text = ""
        link_idx = 0
        for link, chunks in merged_data.items():
            merged_text += f"[link {link_idx + 1}/{len(merged_data)} start]\n{link}\n"
            for i, chunk in enumerate(chunks):
                merged_text += f"[chunk {i+1}/{len(chunks)} start]\n{chunk['text']}\n[chunk {i+1}/{len(chunks)} end]\n"
            merged_text += f"[link {link_idx + 1}/{len(merged_data)} end]\n"
            link_idx += 1

        self.data_store.set_data(DataNames.MERGED_DATA, merged_text)
        self.data_store.set_data(DataNames.LINKS, list(merged_data.keys()))

        self.update_state(TaskStateType.FINISHED, "Merging Finished")
