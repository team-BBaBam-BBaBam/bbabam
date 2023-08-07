from .base_model import ChatModel
from typing import Dict
from datetime import datetime

RESULT_GENERATOR_PROMPT = """
You should output overall answer for the 'User Query'.
3 Information is provided for you : User Query, Instructions, and Result of Searched Social Data.

1. You should answer in the same language as the language of 'User Query'. If 'User Query' is English, you should answer in English, and if it is Korean, you should answer it in Korean. If you get proper nouns as 'User Query', DO NOT try to infer what it describes to specific language. JUST directly recognize the language of User Input.
2. Instruction Indicates does 3 things.
2-1. What information do you need to provide?
2-2. In what format should the answer be written?
2-3. What should you pay attention to when writing the answer?
3. You must follow the instructions, but you do not have to follow the example output if the retrieved data is insufficient to follow the example output.
4. Use searched(given) information rather than your pre-trained insight.
5. You should combine overall informations given, and answer it detailed and high-quality.
6. You should write the answer to be concise and organize information well.
7. You should answer in markdown format.
8. At the end of your answer, you should print the links that you refer to in creating your answer.
8-1. Links should be composed with given 'Result of Searched Social Data'. Links must be naver blog links.
8-2. Links should be printed as following format:
8-2-1. Start with text '[Links]\\n'. (don't contain single quoute, and \\n means line break)
8-2-2. After '[Links]\\n', print your links in list format. Each link text should be surrounded by single quoute.
8-2-3. It will look like this: '[Links]\\n['https://example1.com', 'https://example2.com', 'https://example3.com']'
9. MAKE SURE LANGAUAGE OF YOUR ANSWER IS SAME WITH 'User Query'. This is very important instruction that you MUST follow.
10. The current time is %s, so based on this information, please answer how long the event or deadline is left.
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
            model_type,
            RESULT_GENERATOR_PROMPT
            % str(
                datetime.now().strftime(
                    "year : %Y month : %m day : %d hour : %H minute : %M"
                )
            ),
            temperature,
            stable,
            more_tokens,
        )

    def __repr__(self) -> str:
        return "Result Generation"

    def forward(self, user_input: str, restriction: str, information: str):
        system_prompt = (
            self.system_prompt
            + '\nUser Query: \n"""\n'
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
