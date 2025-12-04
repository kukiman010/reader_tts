# from parser_habr import parser_habr_post
# from pdt_to_text import convert_pdf_to_text
# # import tools
# import book
# import uuid
# from apis.yandex_tts import Yandex_tts
# import speaker

# import media_player



#####################

# from normalizer import Normalizer


# yandex()

# sp = speaker(API_FOLDER)
# line = 'Съешь этих мягких французских булочек да выпей же чаю'
# line2 = 'С 12.01.1943 г. площадь сельсовета — 1785,5 га.'
# line3 = 'В н+едрах т+ундры в+ыдры в г+етрах т+ырят в в+ёдра +ядра к+едров. it is english text'
# text = open('text.txt','r').read()


# # norm = Normalizer()
# # result = norm.norm_text(line2)
# # print(result)

# sp.voice_synthesis_v3(line3, 77777, 'lera')




##################


# userId = 7777
# url = 'https://habr.com/ru/companies/sberbank/articles/888204/'
# # url = 'https://habr.com/ru/companies/otus/articles/886050/'

# pdfFile = parser_habr_post(url, userId)
# outFile = convert_pdf_to_text(pdfFile, userId, False)


# file = open(outFile, 'r', encoding="utf-8")
# data = file.read()
# file.close

# book = book.Book(str(uuid.uuid4()), 'habr', 'other')
# book.load_text(data)
# book.save_to_disk()


# speaker = speaker.Speaker()
# speaker.voice_book_silero(book)
# book.save_to_disk()



# # book = book.Book.load_from_disk('80e91dbb-9bb8-429f-a8cf-8352e64f03d5')

# root = media_player.tk.Tk()
# app = media_player.BookReaderApp(root, book)
# root.mainloop()


###############################################################

# with open("config/mistral.txt", "r", encoding="utf-8") as file:
#             YANDEX_FOLDER = file.read()

# speaker = Yandex_tts(YANDEX_FOLDER)

# text = 'Представляем расширения для браузеров Google Chrome и Mozilla Firefox - теперь с переводом текста'

# speaker.voice_synthesis_v3(text,111)


from parser_habr import parser_habr_post
from pdt_to_text import convert_pdf_to_text
# import tools
import book
import uuid
from apis.yandex_tts import Yandex_tts
import speaker

import media_player

from speaker import Speaker


outFile = convert_pdf_to_text(r'D:\users\bez_raz_v3.pdf', 111, False)



file = open(outFile, 'r', encoding="utf-8")
data = file.read()
file.close



with open(outFile, 'r', encoding='utf-8') as file:
    text = file.read()

local_book = book.Book(str(uuid.uuid4()), 'habr', 'other')
local_book.load_text(text)
local_book.save_to_disk()

speaker = Speaker()
speaker.voice_book_yandex(local_book) 

local_book.save_to_disk()
paths = speaker.merge_and_convert_to_mp3(local_book)



root = media_player.tk.Tk()
app = media_player.BookReaderApp(root, local_book)
root.mainloop()