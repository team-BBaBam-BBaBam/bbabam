from typing import TypedDict, List, Tuple
import tiktoken


class Chunk(TypedDict):
    text: str
    token_count: int


class ChunkDividedText(TypedDict):
    chunks: List[Chunk]
    total_token_count: int
    link: str


class RawText(TypedDict):
    text: str
    link: str


class ChunkDivisor:

    def __init__(self, isGpt3:bool=False):
        self.enc = tiktoken.encoding_for_model(
            "gpt-4" if not isGpt3 else "gpt-3.5-turbo")

    def __split_text(self, text: str, chunk_size: int = 200, chunk_overlap: int = 20) -> List[Tuple[str, int]]:
        '''
        Split text into chunks of tokens, with a sliding window based on the chunk size and overlap.
        text: Text to split
        chunk_size: Maximum token count of each chunk
        chunk_overlap: Overlap token count between chunks
        '''
        splits: List[Tuple[str, int]] = []
        
        encoded = self.enc.encode(text)
        start_idx = 0
        cur_idx = min(start_idx + chunk_size, len(encoded))

        cur_tokens = encoded[start_idx:cur_idx]
        while start_idx < len(encoded):
            splits.append((self.enc.decode(cur_tokens), len(cur_tokens)))
            start_idx += chunk_size - chunk_overlap
            cur_idx = min(start_idx + chunk_size, len(encoded))
            cur_tokens = encoded[start_idx:cur_idx]

        return splits

    def divide_chunks(self, data: List[RawText], chunk_size: int = 400, chunk_overlap: int = 20) -> List[ChunkDividedText]:
        '''
        data: List of RawText
        max_token_count: Maximum token count of each chunk
        return: List of ChunkDividedText
        '''
        divided_texts = []

        for raw_text in data:
            chunks = []
            for chunk, token_count in self.__split_text(raw_text["text"], chunk_size=chunk_size, chunk_overlap=chunk_overlap):
                chunks.append({
                    "text": chunk,
                    "token_count": token_count
                })
            divided_texts.append({
                "chunks": chunks,
                "total_token_count": sum([chunk["token_count"] for chunk in chunks]),
                "link": raw_text["link"]
            })
        return divided_texts
