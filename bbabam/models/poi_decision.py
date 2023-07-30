import re
from .base_model import ChatModel

POI_DESCISION_MAKER_PROMPT = """You will be given "search keyword" and "request in natural language". 
        This inputs might include the context of information user wants to know. 
        You should decide whether POI information is required for this context. 
        POI information is the detailed and static information such as address, operation time and categories of the place. 
        You should output the answer with 1 or 0, 1 is when POI information is needed and 0 is not. 
        And some notes here again. Your return has to include only integer, without any explanation. 
"""


class PoiDecisionMaker(ChatModel):
    def __init__(
        self,
        model_type: str = "gpt-3.5",
        temperature: float = 1.0,
        stable: bool = True,
        more_tokens: bool = False,
    ):
        super.__init__(
            model_type, POI_DESCISION_MAKER_PROMPT, temperature, stable, more_tokens
        )
        print(self.chatmodel)

    def __repr__(self) -> str:
        return "poi_decision_maker"

    def forward(self, keyword: str, user_input: str):
        reply = super().forward(
            f"Search Keyword: {keyword} Request in natural language: {user_input}"
        )

        number = int(re.sub(r"[^0-9]", "", reply.respond))
        return bool(number), reply.respond_with_message, reply.info
