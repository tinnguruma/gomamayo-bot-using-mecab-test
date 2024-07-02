FROM python:3.11
WORKDIR /bot
COPY requirements.txt /bot/
RUN pip install -r requirements.txt
RUN apt-get install mecab libmecab-dev mecab-ipadic-utf8
COPY . /bot
CMD python main.py
