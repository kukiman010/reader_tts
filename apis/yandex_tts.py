# http://yandex.cloud/en-ru/docs/iam/operations/api-key/create#cli_2

from speechkit import model_repository, configure_credentials, creds
import soundfile as sf
import sys
import io
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools import get_time_string



class Yandex_tts:
    def __init__(self):
        with open("config/yandex_tts.key", "r", encoding="utf-8") as file:
            self.api_key = file.read()
        configure_credentials(
            yandex_credentials=creds.YandexCredentials(
                api_key=self.api_key
            )
        )


    def speach(self,text, user, speaker='alena'):
        model = model_repository.synthesis_model()

        model.voice = speaker
        model.role = 'good'

        # Синтез речи и создание аудио с результатом.
        result = model.synthesize(text, raw_format=False) # returns audio as pydub.AudioSegment

        formatted_datetime = get_time_string()
        filename_wav = f'send_voice_{user}_{formatted_datetime}.wav'
        file_path = f'./audio_output/{filename_wav}'

        # Экспортируем AudioSegment в файл
        # result.export(file_path, format="wav")

        # Получаем байты из AudioSegment
        buffer = io.BytesIO()
        result.export(buffer, format="wav")
        data_bytes = buffer.getvalue()

        # Определяем длительность и формат
        with sf.SoundFile(buffer) as audio_file:
            duration_seconds = len(audio_file) / audio_file.samplerate
            file_format = audio_file.format

        # print(file_path)
        
        return data_bytes, duration_seconds, file_format

