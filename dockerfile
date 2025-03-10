# ��пол�з�ем о�и�иал�н�й об�аз Python 3.10
FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Moscow

RUN apt-get update && apt-get install -y ffmpeg

# У��анавливаем �або��� ди�ек�о�и� в кон�ейне�е
WORKDIR /app

# �опи��ем �айл � зави�имо���ми в кон�ейне�
COPY requirements.txt .

# У��анавливаем зави�имо��и
RUN pip install --no-cache-dir -r requirements.txt

# �опи��ем о��ал�ной код п�иложени� в кон�ейне�
COPY . .

# �п�едел�ем команд� зап��ка по �мол�ани�
CMD ["python", "telegram_bot.py"]