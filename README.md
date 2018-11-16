### Демо Azure Speech Service для русского языка
Для демонстрации используется бот в Телеграме, который озвучивает все входящие текстовые сообщений и переводит в текст входящие голосовые.

Для начала работы необходимо:
- скачать код из репозитория
- получить [Azure Speech Service API Key](https://azure.microsoft.com/ru-ru/try/cognitive-services/?api=speech-services)
- создать бота в Телеграме через @BotFather и скопировать токен для бота
- скачать build утилиты [FFmpeg](https://www.ffmpeg.org/download.html)
- в корне проекта файл `config.ini` со следующим текстом:
```
[Azure Speech Service]
API_KEY: <Azure Speech Service API Key>

[Telegram]
API_TOKEN: <API token для Телеграм бота>

[FFMpeg]
PATH_TO_EXE: <путь к ffmpeg.exe>
```
- установить пакеты из файла requirements.txt

После этого можно начинать демонстрацию. Для этого надо запустить файл bot.py