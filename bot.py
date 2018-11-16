#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
import logging.config
import configparser
import requests
import telebot

from tts import text_to_speech
from asr import speech_to_text

TELEGRAM_FILE_URL = 'https://api.telegram.org/file/bot{}/{}'

parser = configparser.ConfigParser()
parser.read('config.ini')

API_TOKEN = parser['Telegram']['API_TOKEN']
telebot.logger.setLevel(logging.INFO)
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def start_msg(message):
    """Обработка команды /start"""

    bot.send_message(
        message.chat.id,
        "Отправьте текстовое сообщение, чтобы услышать его озвучку (Text-To-Speech) "
        "или запишите голосовое сообщение, чтобы получить текст (Speech-To-Text). "
        "\n\nДля работы используется служба Azure Cognitive Services - "
        "[Speech Service](https://docs.microsoft.com/ru-ru/azure/cognitive-services/speech-service/).",
        parse_mode='Markdown'
    )


@bot.message_handler(content_types=['text'])
def synthesize_speech(message):
    """
    Ответ голосовым сообщением, содержащим озвученное
    текстовое сообщение пользователя
    """

    user_name = define_user_name(message.chat)
    print("Запрос на синтез речи от {}".format(user_name))

    file_name = text_to_speech(message.text)

    bot.send_voice(
        message.chat.id,
        open(file_name, 'rb')
    )

    # Удаление WAV файла с речью
    #try:
    #    os.remove(file_name)
    #except:
    #    pass


@bot.message_handler(content_types=['voice'])
def understand_speech(message):
    """
    Ответ текстовым сообщение, отражающим 
    содержание голосового сообщения пользователя
    """

    user_name = define_user_name(message.chat)
    print("Запрос на распознавание речи от {}".format(user_name))

    # Получение содержания голосового запроса
    file_info = bot.get_file(message.voice.file_id)
    file_data = requests.get(TELEGRAM_FILE_URL.format(
        API_TOKEN, file_info.file_path))

    try:
        if file_data.content:
            text = speech_to_text(file_data.content)
            bot.send_message(message.chat.id, text)
        else:
            bot.send_message(message.chat.id, 'Не удалось получить ваш запрос')
    except Exception as ex:
        logging.error(
            'Произошла ошибка во время обработки аудиофайла: {}'.format(repr(ex)))
        bot.send_message(message.chat.id, str(ex))


def define_user_name(chat_info):
    """Формирование никнейма пользователя"""

    user_ids = [id for id in (
        chat_info.username, chat_info.first_name, chat_info.last_name) if id]
    return '-'.join(user_ids) if user_ids else 'unknown-user'


# Запуск бота
bot.polling()
