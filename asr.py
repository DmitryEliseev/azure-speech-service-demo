#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import http.client
import json
import configparser

parser = configparser.ConfigParser()
parser.read('config.ini')

API_KEY = parser['Azure Speech Service']['API_KEY']
VOICE = 'ru-RU'

AccessTokenHost = "westus.api.cognitive.microsoft.com"
path = "/sts/v1.0/issueToken"

STT_URL = "westus.stt.speech.microsoft.com"
STT_URL_PATH = "/speech/recognition/conversation/cognitiveservices/v1"

status_msg = {
    "NoMatch": "В аудиопотоке был обнаружена речь, но не были сопоставлены слова в целевом языке. "
               "Обычно означает, что язык распознавания — это не тот язык, на котором разговаривает пользователь.",
    "InitialSilenceTimeout": "Начало аудиопотока содержит только тишину, и время ожидания на появление речи в службе истекло.",
    "BabbleTimeout": "Начало аудиопотока содержит только шум, и время ожидания на появление речи в службе истекло.",
    "Error": "Служба распознавания обнаружила внутреннюю ошибку и не может продолжить работу. Повторите попытку, если это возможно."
}


def speech_to_text(bin_audio):
    """Перевод речи в текст"""

    params = {
        "language": "ru-RU",
        "format": "simple",
    }

    headers = {
        "Ocp-Apim-Subscription-Key": API_KEY,
        "Content-type": "audio/wav; codec=audio/pcm; samplerate=16000",
        "Accept": "application/json"
    }

    conn = http.client.HTTPSConnection(STT_URL)
    conn.request(
        "POST",
        (
            STT_URL_PATH + "?" +
            "&".join("{}={}".format(key, value)
                     for key, value in params.items())
        ),
        bin_audio,
        headers=headers
    )
    response = conn.getresponse()
    print("ASR", response.status, response.reason)

    res = json.loads(response.read())
    conn.close()

    if response.status == 200:
        if res['RecognitionStatus'] == 'Success':
            return res['DisplayText']
        else:
            msg_error = status_msg.get(res['RecognitionStatus'], None)
            raise Exception(msg_error if msg_error else "Что-то пошло не так")
    else:
        raise Exception(
            "Что-то пошло не так (HTTP CODE {}".format(response.status))
