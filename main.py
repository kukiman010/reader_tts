from parser_habr import parser_habr_post
from pdt_to_text import convert_pdf_to_text
# import tools
import book
import uuid

import speaker

import media_player



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


userId = 7777
url = 'https://habr.com/ru/companies/sberbank/articles/888204/'
# url = 'https://habr.com/ru/companies/otus/articles/886050/'

pdfFile = parser_habr_post(url, userId)
outFile = convert_pdf_to_text(pdfFile, userId, False)


# outFile = 'media/pdf2txt__7777__20250307_121456_055.txt'

file = open(outFile, 'r', encoding="utf-8")
data = file.read()
file.close

# result = tools.split_text(data)

# result = tools.detect_multiple_languages(data)

# for lang in result:
#        print(f"{lang.lang}: {lang.prob * 100:.2f}%")

# print(result)


# sentences = tools.split_text_sentences(data)
# for i, sentence in enumerate(sentences):

#     print(f"\nПредложение {i+1}:")
#     print(sentence)

###############################################################

book = book.Book(str(uuid.uuid4()), 'habr', 'other')

# text = """
# ## Chapter 1: Beginning
# Однажды, когда мне было шесть лет, я увидел в книге великолепную картинку. На ней был изображен удав, заглатывающий животное.

# ## Chapter 2: The Journey
# Таким образом, я прожил свою жизнь в одиночестве, без кого-либо, с кем я мог бы по-настоящему поговорить.
# """

book.load_text(data)
# book.load_text(text)
book.save_to_disk()


speaker = speaker.Speaker()
speaker.voice_book_silero(book)

book.save_to_disk()



# book = book.Book.load_from_disk('80e91dbb-9bb8-429f-a8cf-8352e64f03d5')

# print()

root = media_player.tk.Tk()
app = media_player.BookReaderApp(root, book)
root.mainloop()