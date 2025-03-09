import telebot
import re
import uuid, time
from speaker import Speaker
# from book import Book
# import speaker
import book

from parser_habr import parser_habr_post
from pdt_to_text import convert_pdf_to_text



with open('config/telegram.txt', 'r', encoding='utf-8') as file:
    API_TOKEN = file.read()

bot = telebot.TeleBot(API_TOKEN)


HABR_REGEX = re.compile(r'(?:http[s]?://)?(?:www\.)?habr\.com/ru/(?:companies/\w+/)?articles/\d+/')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! пришли ссылку на поста habr и я ее озвучу.")




@bot.message_handler(func=lambda message: HABR_REGEX.match(message.text))
def handle_habr_link(message):
    start_time = time.time() 

    edit_text = "Начинается обработка!"
    sent_message = bot.reply_to(message, edit_text)
    
    chatId = message.chat.id
    pdfFile = parser_habr_post(message.text, chatId)
    outFile = convert_pdf_to_text(pdfFile, chatId, False)

    edit_text += '\n\nСсылка преобразована в текст [100%]'
    bot.edit_message_text(edit_text, chat_id=sent_message.chat.id, message_id=sent_message.message_id)

    with open(outFile, 'r', encoding='utf-8') as file:
        text = file.read()

    edit_text += '\nСоздание книги '
    bot.edit_message_text(edit_text + '[0%]', chat_id=sent_message.chat.id, message_id=sent_message.message_id)
    

    local_book = book.Book(str(uuid.uuid4()), 'habr', 'other')
    local_book.load_text(text)
    local_book.save_to_disk()

    edit_text += '[100%]'
    bot.edit_message_text(edit_text, chat_id=sent_message.chat.id, message_id=sent_message.message_id)

    edit_text += '\nОзвучка текста '
    bot.edit_message_text(edit_text + '[0%]', chat_id=sent_message.chat.id, message_id=sent_message.message_id)

    speaker = Speaker()
    speaker.voice_book_silero(local_book)

    edit_text += '[100%]'
    bot.edit_message_text(edit_text, chat_id=sent_message.chat.id, message_id=sent_message.message_id)

    local_book.save_to_disk()

    edit_text += '\nКонвертирование в один файл '
    bot.edit_message_text(edit_text + '[0%]', chat_id=sent_message.chat.id, message_id=sent_message.message_id)
    path = speaker.merge_and_send_audio_with_soundfile(local_book)
    edit_text += '[100%]'
    bot.edit_message_text(edit_text, chat_id=sent_message.chat.id, message_id=sent_message.message_id)

    # Отправка файла через бота
    with open(path, 'rb') as audio_file:
        bot.send_audio(chatId, audio_file, title=f"{local_book.title} Combined Audio")
        print("Аудиофайл отправлен в Telegram")

    bot.send_document(chatId, open(pdfFile, 'rb'))

    end_time = time.time()
    elapsed_time = end_time - start_time
    edit_text += '\n\nОбработка заняла {:.4f} секунд'.format(elapsed_time)
    bot.edit_message_text(edit_text, chat_id=sent_message.chat.id, message_id=sent_message.message_id)
    # print(f"Ввыполнена за {elapsed_time:.4f} секунд")

    






@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Вы сказали: " + message.text + ', а нужно ссылку на пост https://habr.com/ru/feed/')


if __name__ == "__main__":
    bot.polling(none_stop=True)