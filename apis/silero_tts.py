# https://github.com/snakers4/silero-models?tab=readme-ov-file#text-enhancement

import io
import torch
import soundfile as sf
# from pydub import AudioSegment
# from typing import Optional



class Silero:
    def __init__(self, model = 'models/v4_ru.pt', diviceType = 'cpu'):
        self.model = model
        self.device = torch.device(diviceType)
        torch.set_num_threads(4)

        self.model = torch.package.PackageImporter(model).load_pickle("tts_models", "model")
        self.model.to(self.device)


    def speak(self, text, speakerName='baya', sample_rate=48000):
        # Генерация аудио дорожки
        audio_data = self.model.apply_tts(text=text, speaker=speakerName, sample_rate=sample_rate)

        # Использование BytesIO для записи аудио данных
        byte_buffer = io.BytesIO()
        sf.write(byte_buffer, audio_data, sample_rate, format='WAV')
        byte_buffer.seek(0)  # Сброс указателя на начало буфера

        # Чтение аудио данных из буфера
        with sf.SoundFile(byte_buffer) as audio_file:
            duration_seconds = len(audio_file) / audio_file.samplerate
            file_format = audio_file.format

        # Получение байтов из буфера
        data_bytes = byte_buffer.getvalue()

        return data_bytes, duration_seconds, file_format