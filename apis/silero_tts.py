# https://github.com/snakers4/silero-models?tab=readme-ov-file#text-enhancement

import io, re
import torch
import soundfile as sf
# from pydub import AudioSegment
# from typing import Optional
import multiprocessing



class Silero:
    def __init__(self, model='models/v4_ru.pt', deviceType='cpu'):
        self.model = model
        self.device = torch.device(deviceType)

        num_cores = 4
        if deviceType == 'cpu':
            num_cores = multiprocessing.cpu_count()
        # elif deviceType == 'gpu':
            # num_cores = 1

        torch.set_num_threads(num_cores)

        self.model = torch.package.PackageImporter(model).load_pickle("tts_models", "model")
        self.model.to(self.device)

    def preprocess_text(self, text):
        # Пример функции замены чисел на текстовые аналоги
        num_to_text = {
            '0': 'ноль', '1': 'один', '2': 'два', '3': 'три', '4': 'четыре',
            '5': 'пять', '6': 'шесть', '7': 'семь', '8': 'восемь', '9': 'девять'
        }

        # Замена каждого числа внутри строки
        def replace_match(match):
            return num_to_text[match.group(0)]

        # Замена всех цифр в тексте
        processed_text = re.sub(r'\d', replace_match, text)
        return processed_text

    def speak(self, text, speakerName='baya', sample_rate=48000):
        # Предобработка текста
        text = self.preprocess_text(text)

        try:
            # Попытка генерации аудио
            audio_data = self.model.apply_tts(text=text, speaker=speakerName, sample_rate=sample_rate)

            # Использование BytesIO для записи аудио данных
            byte_buffer = io.BytesIO()
            sf.write(byte_buffer, audio_data, sample_rate, format='WAV')
            byte_buffer.seek(0)  # Сброс указателя на начало буфера

            # Чтение аудио данных из буфера
            with sf.SoundFile(byte_buffer) as audio_file:
                duration_seconds = len(audio_file) / audio_file.samplerate
                file_format = audio_file.format
        except ValueError as e:
            # Обработка ошибки и создание пустого аудиофайла
            print(f"Ошибка при обработке текста: {e}")
            byte_buffer = io.BytesIO()
            sf.write(byte_buffer, [], sample_rate, format='WAV')  # Пустой аудиофайл
            byte_buffer.seek(0)
            duration_seconds = 0
            file_format = 'WAV'

        # Получение байтов из буфера
        data_bytes = byte_buffer.getvalue()

        return data_bytes, duration_seconds, file_format