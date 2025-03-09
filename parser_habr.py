import requests
from bs4 import BeautifulSoup
from weasyprint import HTML
from tools import get_time_string


def parser_habr_post(url, userId):
    
    fileName = 'habrPost__{}__{}.pdf'.format(userId, get_time_string())
    pdfWay = 'media/' + fileName
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Ищем блок статьи
    article_block = soup.find('article', class_='tm-article-presenter__content')

    # Проверяем, что статья найдена
    if article_block is not None:
        # Преобразуем HTML блок в строку
        article_html = str(article_block)
        
        style = """
        <style>
            img { max-width: 600px; height: auto; } 
        </style>
        """

        # style = """
        # <style>
        # .tm-article-presenter__content {
        #     font-family: 'Fira Sans', sans-serif;
        #     color: #333;
        #     line-height: 1.6;
        #     font-size: 16px;
        #     margin: 20px;
        # }
        # .tm-article-presenter__content img {
        #     max-width: 100%;
        #     height: auto;
        # }
        # </style>
        # """


        
        HTML(string=style + article_html).write_pdf(pdfWay)
        print("PDF файл успешно создан!")
        return pdfWay
    else:
        print("Не удалось найти статью на странице.")
        return None