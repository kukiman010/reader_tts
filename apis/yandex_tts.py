import subprocess
import threading
import base64
import time
import json
import re
import io
import soundfile as sf



class Yandex_tts:
    def __init__(self, TOKEN_FOLDER_ID):
        with open("config/yandex.txt", "r", encoding="utf-8") as file:
            self.t_folder_id = file.read()
        # self.t_folder_id = TOKEN_FOLDER_ID
        self.stop_event = threading.Event()
        self.ready_token = True
        self.TIME_GEN=18000 # once to timer (18000 = 5 hours)

        self.t_IAM = self.create_iam()
        if self.t_IAM == '':
            self.ready_token = False
            print("Токен IAM не создался ")
        else:
            print("Токен IAM cоздан!")


    
    def get_time_string(self):
        current_time = time.time()
        time_struct = time.localtime(current_time)
        # return time.strftime("%Y%m%d_%H%M%S", time_struct)
        milliseconds = int((current_time - int(current_time)) * 1000)
        return time.strftime("%Y%m%d_%H%M%S", time_struct) + f"_{milliseconds:03d}"
    
    
    def create_iam(self):
        output = subprocess.check_output('yc iam create-token', shell=True, universal_newlines=True)
        lines = output.split("\n")
        pattern = r"^(t1.+)$"

        if len(lines) >2:
            print("Не ожаданный результат, нужно проверить вывод \'yc iam create-token\' \nВывод: {}".format(lines))
            # print("Не ожаданный результат, нужно проверить вывод \'yc iam create-token\' \nВывод: {}".format(lines))
        
        for line in lines:
            match = re.findall(pattern, line)
            if match:
                return str(match[0])
            
        return ""
    

    def voice_synthesis_v3(self, text, user, speaker='alena'):
        json_str =  json.dumps({
            "text": text,
            "outputAudioSpec": {
            "containerAudio": {"containerAudioType": "WAV"}
            },
            "hints": [
                {"voice": speaker},
                {"role": "neutral"}
            ],
            "loudnessNormalizationType": "LUFS"
        })
        json_obj = json.loads(json_str)

        command = [
            'grpcurl',
            '-H', f'authorization: Bearer {self.t_IAM}',
            '-H', f'x-folder-id: {self.t_folder_id}',
            '-d', '@',
            'tts.api.cloud.yandex.net:443',
            'speechkit.tts.v3.Synthesizer/UtteranceSynthesis'
        ]
        proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate(json_str.encode('utf-8'))

        json_obj = json.loads(stdout)
        audio_data = json_obj['audioChunk']['data']

        formatted_datetime = self.get_time_string()
        filename = 'send_voice_{}_{}.ogg'.format(user, formatted_datetime)

        # Конвертация из base64 в wav
        audio_bytes = base64.b64decode(audio_data)
        with open('./audio_output/' + filename, 'wb') as file:
            file.write(audio_bytes)

        return str('./audio_output/' + filename)




    def speak(self, text, speaker='alena'):
        if not text or not isinstance(text, str):
                print("Invalid text input.")
                return None, 0, 'Unknown'

        json_str =  json.dumps({
            "text": text,
            "outputAudioSpec": {
            "containerAudio": {"containerAudioType": "WAV"}
            },
            "hints": [
                {"voice": speaker},
                {"role": "neutral"}
            ],
            "loudnessNormalizationType": "LUFS"
        })
        json_obj = json.loads(json_str)

        command = [
         'C:\\Path\\To\\grpcurl.exe',  # Укажите полный путь к grpcurl
         '-H', f'authorization: Bearer {self.t_IAM}',
         '-H', f'x-folder-id: {self.t_folder_id}',
         '-d', '@',
         'tts.api.cloud.yandex.net:443',
         'speechkit.tts.v3.Synthesizer/UtteranceSynthesis'
        ]
        proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        try:
            
            proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = proc.communicate(json_str.encode('utf-8'))

            if proc.returncode != 0:
                print(f"gRPC request failed with error: {stderr.decode('utf-8')}")
                return None, 0, 'Unknown'

            json_response = json.loads(stdout)
            audio_data = json_response['audioChunk']['data']

            # Конвертация из base64 в raw audio bytes
            audio_bytes = base64.b64decode(audio_data)




            # Использование BytesIO для обработки аудиоданных в памяти
            byte_buffer = io.BytesIO(audio_bytes)
            with sf.SoundFile(byte_buffer) as audio_file:
                duration_seconds = len(audio_file) / audio_file.samplerate
                file_format = audio_file.format

            # Сброс указателя на начало буфера
            byte_buffer.seek(0)
            data_bytes = byte_buffer.read()

            return data_bytes, duration_seconds, file_format

        except Exception as e:
            print("An error occurred during voice synthesis.")
            # Возвращаем пустое значение при возникновении ошибки
            return None, 0, 'Unknown'

