from .base_model import ChatModel
from typing import Dict

RESULT_GENERATOR_PROMPT = """
You should output overall answer for the "Traveler Questions".
3 Information is provided for you : "Traveler Questions", instructions, and the result of searched social data.

1. You should answer in the same language as the language of "Traveler Questions". If "Traveler Questions" is English, you should answer in English, and if it is Korean, you should answer it in Korean. If you get proper nouns as User Input, DO NOT try to infer what it describes to specific language. JUST directly recognize the language of User Input.
2. Instruction Indicates does 3 things.
2-1. What information do you need to provide?
2-2. In what format should the answer be written?
2-3. What should you pay attention to when writing the answer?
3. You must follow the instructions, but you do not have to follow the example output if the retrieved data is insufficient to follow the example output.
4. Use searched(given) information rather than your pre-trained insight.
5. You should combine overall informations given, and answer it detailed and high-quality.
6. You should write the answer to be concise and organize information well.
7. You should Include url link where you refer in your anwser.
7-1. URL links should be composed with given 'Result of Searched Social Data'. URL must be naver blog links.
7-2. Your URL links output should be located at very end of the overall output and formed as following example:
    [Links]
    ['https://blog.naver.com/aaa/111', 'https://blog.naver.com/bbb/222', 'https://blog.naver.com/ccc/333'...]
8. MAKE SURE LANGAUAGE OF YOUR ANSWER IS SAME WITH "Traveler Questions". This is very important instruction that you MUST follow.
"""


class ResultGenerator(ChatModel):
    def __init__(
        self,
        model_type: str = "gpt-3.5",
        temperature: float = 0.2,
        stable: bool = True,
        more_tokens: bool = True,
    ):
        super().__init__(
            model_type, RESULT_GENERATOR_PROMPT, temperature, stable, more_tokens
        )

    def __repr__(self) -> str:
        return "Result Generation"

    def forward(self, user_input: str, restriction: str, information: str):
        system_prompt = (
            self.system_prompt
            + "\nTraveler Questions: \n\"\"\"\n"
            + user_input
            + "\n\"\"\"\n"
            + "Instruction:  \n\"\"\"\n"
            + restriction
            + "\n\"\"\"\n"
        )

        user_input = "Result of Searched Data: \n\"\"\"\n" + information + "\n\"\"\"\n"

        reply = super().forward(
            user_input,
            get_system_prompt=lambda: system_prompt,
        )

        return reply.respond, reply.respond_with_message, reply.info
