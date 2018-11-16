### ���� Azure Speech Service ��� �������� �����
��� ������������ ������������ ��� � ���������, ������� ���������� ��� �������� ��������� ��������� � ��������� � ����� �������� ���������.

��� ������ ������ ����������:
- ������� ��� �� �����������
- �������� [Azure Speech Service API Key](https://azure.microsoft.com/ru-ru/try/cognitive-services/?api=speech-services)
- ������� ���� � ��������� ����� @BotFather � ����������� ����� ��� ����
- ������� build ������� [FFmpeg](https://www.ffmpeg.org/download.html)
- � ����� ������� ���� `config.ini` �� ��������� �������:
```
[Azure Speech Service]
API_KEY: <Azure Speech Service API Key>

[Telegram]
API_TOKEN: <API token ��� �������� ����>

[FFMpeg]
PATH_TO_EXE: <���� � ffmpeg.exe>
```
- ���������� ������ �� ����� requirements.txt

����� ����� ����� �������� ������������. ��� ����� ���� ��������� ���� bot.py