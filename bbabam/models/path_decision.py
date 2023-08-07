from .base_model import ChatModel

PATH_DATA_EXTRACTOR_PROMPT = """Two Information is provided for you : Traveler Questions, and the Answer of Traveler Questions.
The Answer of Traveler Questions was attributed to Traveler Questions. Simply you can understand the Answer of Traveler Questions is to solve needs in Traveler Questions.
Your task is to output if you would think that user needs pathfinding data from A to B, the two place name data A and B.

1. You should output in Korean words, even if it is described as other language. For example, you can result in ['경복궁', '북촌한옥마을'], but you MUST NOT output like ['Gyoungbokgung', 'Buk-chon hanok village'].
1-1. Usually place data are proper nouns. Don't try to generalize in common nouns.
2. Output should be formed as ['장소1', '장소2'] at pathfinding. Ensure that pathfinding has to only result in one pair of the startpoint and endpoint.
2-1. First index in list is startpoint, and second one is endpoint of pathfinding.
2-3. Any informations are unnessasary, just output as: []
3. In pathfinding, sometimes Answer of Traveler Questions can contain wrong informations. So if you can result in startpoint and endpoint directly from 'Traveler Questions', you should directly output them.
"""


class PathDataExtractor(ChatModel):
    def __init__(
        self,
        model_type: str = "gpt-4",
        temperature: float = 0.2,
        stable: bool = True,
    ):
        super().__init__(model_type, PATH_DATA_EXTRACTOR_PROMPT, temperature, stable)

    def __repr__(self) -> str:
        return "Path Keyword Generation"

    def forward(self, user_input: str, result: str):
        system_prompt = (
            self.system_prompt
            + '\nTraveler Questions: \n"""\n'
            + user_input
            + '\n"""\n',
        )

        user_input = 'Result of Searched Data: \n"""\n' + result + '\n"""\n'

        reply = super().forward(
            user_input,
            get_system_prompt=lambda: system_prompt,
        )

        return reply.respond, reply.respond_with_message, reply.info
