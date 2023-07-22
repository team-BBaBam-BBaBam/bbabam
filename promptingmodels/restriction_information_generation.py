from typing import Tuple, List, Dict, Union
from settings.openailm import Openai_chat_model, CHATGPT_4_MODEL_STABLE, CHATGPT_3_MODEL_STABLE

sys_prompt = '''You will be given 'search keyword' to get information.  Customers want answers to their search keywords.  The attendant will be responsible for providing answers to the customer.  You must write down the Instructions to be delivered to the attendant.
 

Condition:
1. The attendant will not know about the 'search keyword', and will write an answer only by looking at your Instruction.
2. The attendant will write the answer in text.
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


Your output MUST follow this format:
'{instruction}' MUST be replaced with your written instruction. Your written instruction MUST be surrounded by """.  You should respond once and it will look like:
Instruction:
"""
{instruction}
"""
'''


class RestrictionInformationGenerator:
    '''
    사용자가 입력한 질의문을 바탕으로, 이에 대한 제한사항(Instruction) 글을 생성하는 모듈
    '''

    def __init__(self, use_gpt3: bool = False, openai_chat_model: Union[Openai_chat_model, None] = None):
        if openai_chat_model is None:
            self.__openai_chat_model = Openai_chat_model(
                CHATGPT_3_MODEL_STABLE if use_gpt3 else CHATGPT_4_MODEL_STABLE)
        else:
            self.__openai_chat_model = openai_chat_model

    def __create_messages(self, user_input: str) -> List[Dict[str, str]]:
        return [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": f'Given search keyword:\n"""\n{user_input}\n"""'}
        ]

    def __process_raw_response(self, raw_response: str) -> Tuple[bool, str]:
        '''
        raw_response: OpenAI API로부터 받은 raw response
        return: (is_success, processed_response)
        '''
        raw_response = raw_response.strip()
        if not raw_response.startswith("Instruction:"):
            return False, ""

        processed_response = raw_response[len("Instruction:"):].strip()
        if not processed_response.startswith('"""') or not processed_response.endswith('"""'):
            return False, ""

        processed_response = processed_response[3:-3].strip()
        return True, processed_response

    def generate_restriction(self, user_input: str) -> str:
        '''
        user_input: 사용자가 입력한 검색 키워드
        return: Instruction (str) or "" (str) (실패시)
        '''
        messages = self.__create_messages(user_input)
        completion = self.__openai_chat_model.get_completion(messages)
        # TODO: Handle Failed Response Case
        response = completion["choices"][0]["message"]["content"]
        is_success, processed_response = self.__process_raw_response(response)
        if not is_success:
            return ""
        return processed_response
