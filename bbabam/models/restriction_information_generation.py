from typing import Tuple, List, Dict, Union
from .base_model import ChatModel

RESTRICTION_INFORMATION_GENERATOR_PROMPT = """You will be given 'search keyword' to get information.  Customers want answers to their search keywords.  The attendant will be responsible for providing answers to the customer.  You must write down the Instructions to be delivered to the attendant.
 

Conditions:
1. The attendant will not know about the 'search keyword', and will write an answer only by looking at your Instruction.
2. The attendant will write the answer in markdown format text.
3. Attendants should write as detailed and high-quality answers as possible.
4. The Instruction you write should contain the following information.
4-1.  What information do you need to provide?
4-2.  In what format should the answer be written?
4-3.  What should I pay attention to when writing my answer?
5. Instructions should be written concisely, including only the essentials.
6. In Instruction, you should use 'you' when referring to an 'attendant', and 'user' when referring to a 'customer'.
7. Do not use the words 'attendant' or 'customer' in the Instructions.
8. If necessary, it is okay to provide the example text format(answer template) of the answer in the Instruction. You SHOULD NOT include actual contents in example text format.
9. Instructions must be written in English.
10. Attendants will write answers in the same language as the 'search keyword'. Keep this in mind when writing your answer template.
11. When you use numbering in your instruction, start number from 1.
12. Your output must follow this format:
12-1. Start with text 'Instruction:\n'. (don't contain single quoute, and \\n means line break)
12-2. After 'Instruction:\\n', print your Instruction and it should be surrounded by triple double quotes('\"\"\"\\n...\\n\"\"\"')
12-3. It will look like this: 'Instruction:\\n\"\"\"\\n...\\n\"\"\"'
12-4. Do not print other descriptions that violate the above format.
12-5. You have to answer only once.
13. Write answer in less than 100 words.
"""


class RestrictionInformationGenerator(ChatModel):
    """
    사용자가 입력한 질의문을 바탕으로, 이에 대한 제한사항(Instruction) 글을 생성하는 모듈
    """

    def __init__(
        self,
        model_type: str = "gpt-3.5",
        temperature: float = 0.7,
        stable: bool = True,
        more_tokens: bool = False,
    ):
        super().__init__(
            model_type,
            RESTRICTION_INFORMATION_GENERATOR_PROMPT,
            temperature,
            stable,
            more_tokens,
        )

    def __repr__(self) -> str:
        return "Restriction information Generation Module"

    def __process_raw_response(self, raw_response: str) -> Tuple[bool, str]:
        """
        raw_response: OpenAI API로부터 받은 raw response
        return: (is_success, processed_response)
        """
        raw_response = raw_response.strip()
        if not raw_response.startswith("Instruction:"):
            return False, ""

        processed_response = raw_response[len("Instruction:") :].strip()
        if not processed_response.startswith('"""') or not processed_response.endswith('"""'):
            return False, ""

        processed_response = processed_response[3:-3].strip()
        return True, processed_response

    def forward(self, user_input: str) -> str:
        """
        user_input: 사용자가 입력한 검색 키워드
        return: Instruction (str) or "" (str) (실패시)
        """
        reply = super().forward(f'Given search keyword:\n"""\n{user_input}\n"""')
        # TODO: Handle Failed Response Case
        response = reply.respond
        is_success, processed_response = self.__process_raw_response(response)
        if not is_success:
            print("Failed to process response")
            print("Response: ", response)
            return "", reply.respond_with_message, reply.info

        return processed_response, reply.respond_with_message, reply.info
