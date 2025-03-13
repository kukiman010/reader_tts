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
        # with open("config/mistral.txt", "r", encoding="utf-8") as file:
            # YANDEX_FOLDER = file.read()

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

        # Обходим все предложения из книги
        for sentence in book.iter_sentences():
            if sentence.audio_path:
                data, current_samplerate = sf.read(sentence.audio_path)
                if samplerate is None:
                    samplerate = current_samplerate
                elif samplerate != current_samplerate:
                    raise ValueError("Все аудиофайлы должны иметь одинаковую частоту дискретизации")

                if combined_data.size == 0:
                    combined_data = data
                else:
                    combined_data = np.concatenate((combined_data, data))

        if combined_data.size == 0:
            print("Не удалось объединить: нет доступных аудиофайлов.")
            return

        # Преобразование numpy массива в байты
        wav_bytes_io = io.BytesIO()
        sf.write(wav_bytes_io, combined_data, samplerate, format='WAV')
        wav_bytes_io.seek(0)  # Важный шаг: перемещаем указатель на начало io.BytesIO объекта

        # Конвертация в MP3 с использованием байтовых данных
        audio_segment = AudioSegment.from_file(wav_bytes_io, format='wav')
        output_mp3_path = output_dir / f"{book.book_id}_combined.mp3"
        audio_segment.export(output_mp3_path, format="mp3", bitrate="192k")
        # print(f"Сохранённый MP3 файл: {output_mp3_path}")

        return output_mp3_path




# import uuid

# text = '## Глава 1: Неожиданный гость\
# Во время прогулки по густому лесу, Алекс наткнулся на мерцающую тропинку, которую раньше не замечал.\
# ## Глава 2: Свет в глубине леса \
# Следуя по тропинке, он оказался перед величественным дубом, от которого исходило странное сияние.\
# ## Глава 3: Голос из темноты \
# Внезапно из глубины леса раздался мягкий голос, предлагая Алексу исполнить самое заветное желание. \
# ## Глава 4: Исчезновение \
# Не успев осознать происходящее, Алекс моргнул и обнаружил себя на опушке леса, держа в руке загадочный старинный амулет. '

# text = '## Глава 1: Неожиданный гость\
# Во время прогулки по густому лесу, Алекс наткнулся на мерцающую тропинку, которую раньше не замечал.\
# ## Глава 2: Свет в глубине леса \
# Следуя по тропинке, он оказался перед величественным дубом, от которого исходило странное сияние.'

# book = book.Book(str(uuid.uuid4()), 'habr', 'other')
# book.load_text(text)
# book.save_to_disk()

# speaker = Speaker()
# # speaker.voice_book_silero(book)
# speaker.voice_book_yandex(book)

# book.save_to_disk()