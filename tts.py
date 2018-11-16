#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Source: https://github.com/Azure-Samples/Cognitive-Speech-TTS/blob/master/Samples-Http/Python/TTSSample.py
# Source: https://docs.microsoft.com/ru-ru/azure/cognitive-services/speech-service/rest-apis

import random
import string
import configparser

import http.client
from xml.etree import ElementTree

from converter import convert_to_ogg

parser = configparser.ConfigParser()
parser.read('config.ini')

API_KEY = parser['Azure Speech Service']['API_KEY']
VOICE = 'ru-RU'

# Voice for russian speech synthesizing
characters = [
    "Irina, Apollo",
    "Pavel, Apollo",
    "EkaterinaRUS"
]

AccessTokenHost = "westus.api.cognitive.microsoft.com"
path = "/sts/v1.0/issueToken"

headers = {
    "Content-type": "application/ssml+xml",
    "X-Microsoft-OutputFormat": "riff-16khz-16bit-mono-pcm",
    "User-Agent": "TTSForPython"
}


def text_to_speech(text: str):
    """Перевод текста в речь"""

    # Connect to server to get the Access Token
    conn = http.client.HTTPSConnection(AccessTokenHost)
    conn.request("POST", path, headers={"Ocp-Apim-Subscription-Key": API_KEY})
    response = conn.getresponse()
    accesstoken = response.read().decode("UTF-8")
    conn.close()
    print("1.TTS", response.status, response.reason)

    # Setting for speech synthesizing
    body = ElementTree.Element('speak', version='1.0')
    body.set('{http://www.w3.org/XML/1998/namespace}lang', VOICE.lower())
    voice = ElementTree.SubElement(body, 'voice')
    voice.set('{http://www.w3.org/XML/1998/namespace}lang', VOICE)
    voice.set('name', 'Microsoft Server Speech Text to Speech Voice ({}, {})'.format(
        VOICE, characters[1]))
    voice.text = text

    # Connect to server to synthesize the wave
    conn = http.client.HTTPSConnection("westus.tts.speech.microsoft.com")

    # Добавление нового хэдера
    headers["Authorization"] = "Bearer " + accesstoken

    conn.request("POST", "/cognitiveservices/v1",
                 ElementTree.tostring(body), headers)
    response = conn.getresponse()
    print("2.TTS", response.status, response.reason)
    data = response.read()
    conn.close()

    file_name = ''.join(random.choices(
        string.ascii_lowercase + string.digits, k=7)) + '.wav'
    with open(file_name, 'wb') as file:
        file.write(convert_to_ogg(in_content=data))

    return file_name
