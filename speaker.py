from apis.yandex_tts import Yandex_tts
from apis.silero_tts import Silero
# from apis.coqui_tts import coque
# from apis.openai_tts import openai
from pathlib import Path
import book
import numpy as np
import soundfile as sf
from pydub import AudioSegment
import io

MAX_FILE_SIZE_MB = 45
BYTES_PER_MB = 1024 * 1024
import os

BITRATE = "96k"

class Speaker:
    # def __init__(self):
    #     self.api_key = api_key
    #     self.voice = voice
    #     self.format = format
    #     self.cache = {}  # Кэш для избежания повторной генерации

    def check_api(): # проверяет доступность сервисов
        print()

    # def synthesize(self, text: str) -> tuple[bytes, float]:
    #     # Заглушка для реальной реализации TTS API
    #     # В реальности здесь будет подключение к API типа Google Cloud Text-to-Speech
    #     audio_data = f"fake_audio_{hash(text)}".encode()
    #     duration = len(text) * 0.1  # Примерная продолжительность
    #     return audio_data, duration


    def voice_book_silero(self, book):
        book.add_metadata('speaker', 'Yandex')
        speaker = Silero()

        sentences = list(book.iter_sentences())  # Преобразуем итератор в список, чтобы узнать общее количество предложений
        total_sentences = len(sentences)

        for index, sentence in enumerate(sentences):
            data_audio, duration, file_format = speaker.speak(sentence.text)

            audio_filename = f"ch{sentence.chapter_id}_s{sentence.position}.{file_format}"
            audio_path = Path(book.storage_path) / "audio" / audio_filename
            
            audio_path.parent.mkdir(exist_ok=True, parents=True)
            audio_path.write_bytes(data_audio)
            
            sentence.audio_path = str(audio_path)
            sentence.audio_format = file_format
            sentence.audio_duration = duration

            # Расчет и вывод процента выполнения
            percent_completed = (index + 1) / total_sentences * 100
            print(f"\rПроцент выполнения: {percent_completed:.2f}%", end='')
            # sys.stdout.flush()  # Обеспечиваем немедленный вывод на экран

    def voice_book_yandex(self, book ):
        book.add_metadata('speaker', 'Yandex')
        speaker = Yandex_tts()

        sentences = list(book.iter_sentences())  # Преобразуем итератор в список, чтобы узнать общее количество предложений
        total_sentences = len(sentences)

        for index, sentence in enumerate(sentences):
            data_audio, duration, file_format = speaker.speach(sentence.text, 77777)

            audio_filename = f"ch{sentence.chapter_id}_s{sentence.position}.{file_format}"
            audio_path = Path(book.storage_path) / "audio" / audio_filename
            
            audio_path.parent.mkdir(exist_ok=True, parents=True)
            audio_path.write_bytes(data_audio)
            
            sentence.audio_path = str(audio_path)
            sentence.audio_format = file_format
            sentence.audio_duration = duration

            # Расчет и вывод процента выполнения
            percent_completed = (index + 1) / total_sentences * 100
            print(f"\rПроцент выполнения: {percent_completed:.2f}%", end='')


    def merge_and_convert_to_mp3(self, book):
        output_dir = Path('audio_output')
        output_dir.mkdir(exist_ok=True)

        combined_data = np.array([])
        samplerate = None

        for sentence in book.iter_sentences():
            if sentence.audio_path:
                data, current_samplerate = sf.read(sentence.audio_path)
                if samplerate is None:
                    samplerate = current_samplerate
                elif samplerate != current_samplerate:
                    raise ValueError("Sample rate mismatch")
                combined_data = np.concatenate((combined_data, data))
        
        if combined_data.size == 0:
            print("Не удалось объединить: нет аудиофайлов")
            return []

        wav_bytes_io = io.BytesIO()
        sf.write(wav_bytes_io, combined_data, samplerate, format='WAV')
        wav_bytes_io.seek(0)

        audio_segment = AudioSegment.from_file(wav_bytes_io, format='wav')

        output_paths = []
        start_ms = 0
        part = 1
        length_ms = len(audio_segment)
        chunk_duration_ms = 60 * 1000 * 5   # стартовый кусок - например, 5 минут

        while start_ms < length_ms:
            chunk = audio_segment[start_ms:start_ms + chunk_duration_ms]
            temp_path = output_dir / f"{book.book_id}_part{part}.mp3"
            chunk.export(temp_path, format="mp3", bitrate=BITRATE)
            size_mb = os.path.getsize(temp_path) / (1024*1024)
            # если кусок получился больше MAX_FILE_SIZE_MB — уменьшаем длину
            while size_mb > MAX_FILE_SIZE_MB and chunk_duration_ms > 20*1000:  # Минимум — 20 сек
                chunk_duration_ms = int(chunk_duration_ms * 0.7)
                chunk = audio_segment[start_ms:start_ms + chunk_duration_ms]
                chunk.export(temp_path, format="mp3", bitrate=BITRATE)
                size_mb = os.path.getsize(temp_path) / (1024*1024)

            output_paths.append(str(temp_path))
            start_ms += chunk_duration_ms
            part += 1

        return output_paths





# import uuid

# text = 'Глава 1: Неожиданный гость\
# Во время прогулки по густому лесу, Алекс наткнулся на мерцающую тропинку, которую раньше не замечал.\
# Глава 2: Свет в глубине леса \
# Следуя по тропинке, он оказался перед величественным дубом, от которого исходило странное сияние.'

# book = book.Book(str(uuid.uuid4()), 'habr', 'other')
# book.load_text(text)
# book.save_to_disk()

# speaker = Speaker()
# # speaker.voice_book_silero(book)
# speaker.voice_book_yandex(book)

# book.save_to_disk()



