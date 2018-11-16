#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from ffmpy import FFmpeg
import subprocess
import configparser

parser = configparser.ConfigParser()
parser.read('config.ini')


def run_ffmpeg(ff_inputs, ff_outputs, in_filename: str = None, in_content: bytes = None):
    """Обобщённый метод для вызова ffmpeg"""

    ff = FFmpeg(
        executable=parser['FFMpeg']['PATH_TO_EXE'],
        inputs=ff_inputs,
        outputs=ff_outputs
    )
    if in_filename:
        in_content = open(in_filename, 'br').read()
    else:
        in_filename = "No file, just bytes"

    if not in_content:
        raise Exception("Не могу получить контент из {}".format(in_filename))

    stdout = ff.run(
        input_data=in_content,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )[0]

    return stdout


def convert_to_ogg(in_filename: str = None, in_content: bytes = None):
    """Конвертирование файл/байтов в OOG кодировку (необходимую для Telegram)"""

    return run_ffmpeg(
        {'pipe:0': None},
        {'pipe:1': ['-f', 'ogg', '-acodec', 'libopus']},
        in_filename,
        in_content
    )


def convert_to_pcm16b16000r(in_filename=None, in_content=None):
    """Конвертирование файл/байтов в WAV моно PCM 160000 Гц 16 бит"""

    return run_ffmpeg(
        {'pipe:0': None},
        {'pipe:1': ['-f', 's16le', '-acodec',
                    'pcm_s16le', '-ac',  '1', '-ar', '16000']},
        in_filename,
        in_content
    )
