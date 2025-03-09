# https://github.com/coqui-ai/TTS

import torch
from TTS.api import TTS

INPUT_EN_PATH = '/home/sysadm/python/tts_test/input_voice.mp3'
INPUT_RU_PATH = 'audio_input/input_voice_ru.mp3'

TEXT_EN = 'A control example for the Russian text. I really want more of these soft, crispy French buns.'
TEXT_RU = 'Рома, ну конечно я тебе куплю робинсон'
TEXT_RU2 = 'В лесу под луной, где светят росы,  Забавный лисёнок гуляет между сосен.  Он хитрый и ловкий, как светлый огонь,  Словно танцует в тени он, как зной.  Его мех – как закат, что играет с огнем,  Блестит и пылает, ласкает теплом.  Глаза его — звёзды, что ярко горят,  Секреты лесные в них говорят. Он скачет по тропам в ночной тишине,  И шепчет историям, скрытым в мгле.  Добрая сказка про лиса-живуна,  Что в сердце у каждого будит весна.'
TEXT_RU3 = 'В н+едрах т+ундры в+ыдры в г+етрах т+ырят в в+ёдра +ядра к+едров. it is english text'

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"
# torch.load()

# List available 🐸TTS models
print(TTS().list_models())

# Init TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

# Run TTS
# ❗ Since this model is multi-lingual voice cloning model, we must set the target speaker_wav and language
# Text to speech list of amplitude values as output
wav = tts.tts(text=TEXT_RU3, speaker_wav=INPUT_RU_PATH, language="ru")
# # Text to speech to a file
tts.tts_to_file(text=TEXT_RU3, speaker_wav=INPUT_RU_PATH, language="ru", file_path="audio_output/coqui_output.mp3")


# OUTPUT_PATH = './out.wav'
# # Init TTS with the target model name
# tts = TTS(model_name="tts_models/de/thorsten/tacotron2-DDC", progress_bar=False).to(device)

# # Run TTS
# tts.tts_to_file(text="Ich bin eine Testnachricht.", file_path=OUTPUT_PATH)

# # Example voice cloning with YourTTS in English, French and Portuguese
# tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts", progress_bar=False).to(device)
# tts.tts_to_file("This is voice cloning.", speaker_wav="my/cloning/audio.wav", language="en", file_path="output.wav")
# tts.tts_to_file("C'est le clonage de la voix.", speaker_wav="my/cloning/audio.wav", language="fr-fr", file_path="output.wav")
# tts.tts_to_file("Isso é clonagem de voz.", speaker_wav="my/cloning/audio.wav", language="pt-br", file_path="output.wav")