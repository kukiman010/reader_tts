# from apis.yandex_tts import Yandex
from apis.silero_tts import Silero
# from apis.coqui_tts import coque
# from apis.openai_tts import openai
from pathlib import Path
import book



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


