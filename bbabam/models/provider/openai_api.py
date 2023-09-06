from bbabam.settings.environment import OpenAIKeys
from bbabam.settings.errors import NotProvidedModelError
from typing import Dict, List
from dataclasses import dataclass
import openai

OpenAIKeys().init()

CHATGPT_3_MODEL = "gpt-3.5-turbo"
CHATGPT_3_MODEL_16K = "gpt-3.5-turbo-16k"
CHATGPT_3_MODEL_STABLE = "gpt-3.5-turbo-0613"
CHATGPT_3_MODEL_16K_STABLE = "gpt-3.5-turbo-16k-0613"
CHATGPT_4_MODEL = "gpt-4"
CHATGPT_4_MODEL_32K = "gpt-4-32k"
CHATGPT_4_MODEL_STABLE = "gpt-4-0613"
CHATGPT_4_MODEL_32K_STABLE = "gpt-4-32k-0613"
WORD_EMBEDDING_MODEL = "text-embedding-ada-002"
MessageType = List[Dict[str, str]]

OPENROUTER_REFERRER = "https://github.com/alonsosilvaallende/chatplotlib-openrouter"


def getModelName(model_type: str, stable: bool = False, more_tokens: bool = False):
    # 모델을 편하게 선택하기 위한 클래스
    # model의 가능한 인풋은 gpt-3.5, gpt-4, word-embedding 중에 하나.

    if model_type == "gpt-3.5":
        if stable and more_tokens:
            return CHATGPT_3_MODEL_16K_STABLE
        elif stable and not more_tokens:
            return CHATGPT_3_MODEL_STABLE
        elif not stable and more_tokens:
            return CHATGPT_3_MODEL_16K
        else:
            return CHATGPT_3_MODEL

    elif model_type == "gpt-4":
        if stable and more_tokens:
            return CHATGPT_4_MODEL_32K_STABLE
        elif stable and not more_tokens:
            return CHATGPT_4_MODEL_STABLE
        elif not stable and more_tokens:
            return CHATGPT_4_MODEL_32K
        else:
            return CHATGPT_4_MODEL

    elif model_type == "word-embedding":
        return WORD_EMBEDDING_MODEL
    else:
        raise NotProvidedModelError


@dataclass
class ReturnType:
    respond: str
    message: MessageType
    info: dict


class OpenaiProvider:
    def get(self, messages: MessageType, model, temperature, stream: bool = False):
        completion = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
            headers={"HTTP-Referer": OPENROUTER_REFERRER},
            stream=stream,
        )
        print(completion)
        return ReturnType(
            respond=completion if stream else completion.choices[0].message.content,
            message=None if stream else completion.choices[0].message,
            info={} if stream else completion.usage,
        )
