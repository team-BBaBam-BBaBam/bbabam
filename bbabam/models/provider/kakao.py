from bbabam.settings.environment import OpenAIKeys
from bbabam.settings.errors import NotProvidedModelError

from bbabam.settings.environment import KakaoKeys
from typing import Dict, List
import requests
import json

from dataclasses import dataclass

kakao_key = KakaoKeys()

KAKAO_GPT3_MODEL = "kakao_gpt"
KAKAO_GPT_ENDPOINT = "https://api.kakaobrain.com/v1/inference/kogpt/generation"
MessageType = List[Dict[str, str]]
kakaoRoleDict = {
    "system": "정보:",
    "user": "Q:",
    "assistant": "A",
}


def getModelName(model_type: str, stable: bool = False, more_tokens: bool = False):
    return KAKAO_GPT3_MODEL


@dataclass
class ReturnType:
    respond: str
    message: MessageType
    info: dict


class KakaoProvider:
    def __create_kakao_prompt(self, messages: MessageType) -> str:
        prompt = ""
        for msg in messages:
            prompt += kakaoRoleDict[msg["role"]]
            prompt += msg["content"].replace("\n", " ")
            prompt += "\n"
        prompt += "A:"
        return prompt

    def get(self, messages: MessageType, model: str, temperature: float):
        kakao_prompt = self.__create_kakao_prompt(messages)
        data = {
            "prompt": kakao_prompt,
            "max_tokens": 120,
            "temperature": temperature,
            "n": 1,
            "max_tokens": 256,
        }
        header = {
            "Content-Type": "application/json",
            "Authorization": f"KakaoAK {kakao_key.get_key()}",
        }
        res = requests.post(
            KAKAO_GPT_ENDPOINT,
            headers=header,
            data=json.dumps(data),
        )
        res = res.json()


        return ReturnType(
            respond=res["generations"][0]["text"],
            message=res["generations"][0],
            info=res["usage"],
        )
