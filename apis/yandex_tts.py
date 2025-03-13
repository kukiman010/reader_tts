# http://yandex.cloud/en-ru/docs/iam/operations/api-key/create#cli_2

import subprocess
import threading
import base64
import time
import json
import re
import io
import soundfile as sf

# from .  import tools
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# import tools
from tools import get_time_string


# from argparse import ArgumentParser
from speechkit import model_repository, configure_credentials, creds


class Yandex_tts:
    def __init__(self):
        with open("config/yandex_tts.key", "r", encoding="utf-8") as file:
            self.api_key = file.read()
        configure_credentials(
            yandex_credentials=creds.YandexCredentials(
                api_key=self.api_key
            )
        )


    def speach(self,text, user):
        model = model_repository.synthesis_model()

        # Задайте настройки синтеза.
        model.voice = 'jane'
        model.role = 'good'

        # Синтез речи и создание аудио с результатом.
        result = model.synthesize(text, raw_format=False) # returns audio as pydub.AudioSegment
        # result.export('audio.wav', 'wav')


        formatted_datetime = get_time_string()
        filename_wav = f'send_voice_{user}_{formatted_datetime}.wav'
        file_path = f'./audio_output/{filename_wav}'

        # Экспортируем AudioSegment в файл
        result.export(file_path, format="wav")

        # Получаем байты из AudioSegment
        buffer = io.BytesIO()
        result.export(buffer, format="wav")
        data_bytes = buffer.getvalue()

        # Определяем длительность и формат
        with sf.SoundFile(file_path) as audio_file:
            duration_seconds = len(audio_file) / audio_file.samplerate
            file_format = audio_file.format

        print(file_path)
        
        return data_bytes, duration_seconds, file_format







text = 'кто же этот мистер?'
# speaker = 'alena'


# tts = Yandex_tts()

# way = tts.voice_synthesis_v3(text, 111)
# tts.test(text)


# print(way)


