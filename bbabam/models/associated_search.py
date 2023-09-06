from .base_model import ChatModel
import json

ASSO_SEARCH_PROMPT = """Two Information is provided for you : user input, and the answer of the user input.
The answer of the user input was attributed to user input. Simply you can understand the answer of the user input is to solve needs in user input.
Your task is to output the associated search keyword and following questions for it based on user input and the answer of the user input.

1. You should output it in language same as 'user input'. For example, if the user input was "仁川空港に最も近い両替所は？", You should output "{'為替レート': ['最近円とウォン間の為替レートは？', ...]}"
2. Output should be formed as [{"Keyword1": ["Question1-1", "Question1-2"...]}, {"Keyword2": ["Question2-1", "Question2-2"...]}, ...]
2-1. Keyword has to be word (can be nouns, verbs...), and Questions have to be sentence. So you are composing lists of dictionary that implies words(string) as a key, sentence(also string) as a value.
3. Recommend up to 3 keywords per keyword.
4. Make sure that the search word doesn't exceed 50 characters.
5. You should remind that the users are to travel South Korea. You better output results that can surely acceptable correlation between them(input) and generated dictionary(Your output) on traveler's perspective.
"""


class AssoSearchGenerator(ChatModel):
    def __init__(
        self,
        model_type: str = "gpt-4",
        temperature: float = 0.2,
        stable: bool = True,
    ):
        super().__init__(model_type, ASSO_SEARCH_PROMPT, temperature, stable)

    def __repr__(self) -> str:
        return "Associated Searchs Generation"

    def forward(self, user_input: str, result: str):
        system_prompt = self.system_prompt + '\nUser Input: \n"""\n' + user_input + '\n"""\n'

        user_input = 'Result of Searched Data: \n"""\n' + result + '\n"""\n'

        reply = super().forward(
            user_input,
            get_system_prompt=lambda: system_prompt,
        )

        lod = json.loads(reply.respond)

        return lod, reply.respond_with_message, reply.info
