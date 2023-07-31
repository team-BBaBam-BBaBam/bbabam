from .base_model import ChatModel

PLACE_DATA_EXTRACTOR_PROMPT = """Two Information is provided for you : user input, and the answer of user input.
The answer of user input was attributed to user input. Simply you can understand the answer of user input is to solve needs in user input.
Your task is to result in place data. If specific place data in South Korea has drawn in the answer of user input and you would decide that the user input contains the needs about knowing place data, you should output the list of place name(such as landmarks name, shopping mall, restaurants... and all can be associated with travel).

1. You should output in Korean words, even if it is described as other language. For example, you can result in ['경복궁', '북촌한옥마을', '남산타워'], but you MUST NOT output like ['Gyoungbokgung', 'Buk-chon hanok village', 'Namsan tower'].
1-1. Usually place data are proper nouns. Don't try to generalize in common nouns.
2. Output should be formed as ['장소1', '장소2', '장소3'...].
2-1. Any informations are unnessasary, just output as: []
"""

class PlaceDataExtractor(ChatModel):
    def __init__(
        self,
        model_type: str = "gpt-4",
        temperature: float = 0.2,
        stable: bool = True,
    ):
        super().__init__(
            model_type, PLACE_DATA_EXTRACTOR_PROMPT, temperature, stable
        )

    def __repr__(self) -> str:
        return "Place Keyword Generation"

    def forward(self, user_input: str, result: str):
        system_prompt = (
            self.system_prompt
            + "\nUser Input: \n\"\"\"\n"
            + user_input
            + "\n\"\"\"\n"
        )

        user_input = "Result of Searched Data: \n\"\"\"\n" + result + "\n\"\"\"\n"

        reply = super().forward(
            user_input,
            get_system_prompt=lambda: system_prompt,
        )

        return reply.respond, reply.respond_with_message, reply.info