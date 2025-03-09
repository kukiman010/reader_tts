# from apis.yandex_tts import Yandex
from apis.silero_tts import Silero
# from apis.coqui_tts import coque
# from apis.openai_tts import openai
from pathlib import Path
import book
import numpy as np
import soundfile as sf
from pydub import AudioSegment



class Speaker:
    # def __init__(self, api_key: str, voice: str = "en-US-Wavenet-D", format: str = "mp3"):
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


    def voice_book_silero(self, book: book.Book):
        speaker = Silero()

        for sentence in book.iter_sentences():
            dataAudio, duration, file_format = speaker.speak(sentence.text)

            audio_filename = f"ch{sentence.chapter_id}_s{sentence.position}.{file_format}"
            audio_path = Path(book.storage_path) / "audio" / audio_filename
            
            audio_path.parent.mkdir(exist_ok=True, parents=True)
            audio_path.write_bytes(dataAudio)
            
            sentence.audio_path = str(audio_path)
            sentence.audio_format = file_format
            sentence.audio_duration = duration


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

        # Путь для промежуточного WAV файла
        temp_wav_path = output_dir / f"{book.book_id}_combined.wav"
        sf.write(temp_wav_path, combined_data, samplerate)
        print(f"Промежуточный WAV файл: {temp_wav_path}")

        # Загрузка и конвертация WAV файла в MP3
        audio_segment = AudioSegment.from_wav(temp_wav_path)
        output_mp3_path = output_dir / f"{book.book_id}_combined.mp3"
        audio_segment.export(output_mp3_path, format="mp3", bitrate="192k")
        print(f"Сохранённый MP3 файл: {output_mp3_path}")

        # Удаление промежуточного WAV файла, если он больше не нужен
        temp_wav_path.unlink()

        return output_mp3_path



