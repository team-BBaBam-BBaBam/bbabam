from bbabam.settings.environment import BardKeys
from bardapi import BardCookies
from typing import Dict, List
from dataclasses import dataclass


cookie_dict = {
    "__Secure-1PSID": "ZQgRQpurCAghlQp778TOhys8AwYWHx6TCYITwRg2iyTbiKym3rnNPPa81yKeYMRQN79skQ.",
    "__Secure-1PSIDTS": "sidts-CjEBSAxbGTrv-7sDkd5Eq5o0whHBdtfSaBr4KgGN--u5FIROvvfP9WEMGghxGnU0r2pJEAA",
}


bard_key = BardKeys()
bard = BardCookies(cookie_dict=cookie_dict)

MessageType = List[Dict[str, str]]
bardRoleDict = {
    "system": "system:",
    "user": "question:",
    "assistant": "answer:",
}


@dataclass
class ReturnType:
    respond: str
    message: MessageType
    info: dict


class BardProvider:
    def __create_bard_prompt(self, messages: MessageType) -> str:
        prompt = ""
        for msg in messages:
            prompt += "You are assistant. PLEASE ANSWER ONLY USER'S QUESTIONS. YOU ARE CODES OF MULTIMODAL. IT IS IMPORTANT TO MATCH THE ANSWER TYPE.\n"
            prompt += bardRoleDict[msg["role"]]
            prompt += msg["content"].replace("\n", " ")
            prompt += "\n"
        prompt += "assistant:"
        return prompt

    def get(self, messages: MessageType, model: str, temperature: float):
        bard_prompt = self.__create_bard_prompt(messages)
        res = bard.get_answer(bard_prompt)

        return ReturnType(
            respond=res["content"],
            message=[],
            info={},
        )


def getModelName(model_type: str, stable: bool = False, more_tokens: bool = False):
    return ""
