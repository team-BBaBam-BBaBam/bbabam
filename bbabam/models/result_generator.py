from .base_model import ChatModel
from typing import Dict

RESULT_GENERATOR_PROMPT = """
You should output overall answer for the user input.
3 Information is provided for you : user input, instructions, and the result of searched social data.

1. You should answer in the same language as the language of 'User Input'. Even if the example output in the Instruction is in English, you should write it in the same language as 'User Input'.
2. Instruction Indicates does 3 things.
2-1. What information do you need to provide?
2-2. In what format should the answer be written?
2-3. What should you pay attention to when writing the answer?
3. You must follow the instructions, but you do not have to follow the example output if the retrieved data is insufficient to follow the example output.
4. Use searched(given) information rather than your pre-trained insight.
5. You should combine overall informations given, and answer it detailed and high-quality.
6. You should write the answer to be concise and organize information well.
7. You should Include url link in your anwser if it is necessary.
7-1. URL links should be composed with given 'Result of Searched Social Data', and don't provide urls in 'text' key, only provide from 'link' key. URL must be naver blog links.
7-2. Your URL links output should be located at very end of the overall output and formed as following example:
    [Links]
    [link1, link2, link3, link4...]
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
            + '\nUser Input: \n"""\n'
            + user_input
            + '\n"""\n'
            + 'Instruction:  \n"""\n'
            + restriction
            + '\n"""\n'
        )

        user_input = 'Result of Searched Data: \n"""\n' + information + '\n"""\n'

        reply = super().forward(
            user_input,
            get_system_prompt=lambda: system_prompt,
        )

        return reply.respond, reply.respond_with_message, reply.info
