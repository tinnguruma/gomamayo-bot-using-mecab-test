FROM python:3.9

RUN pip install -U pip

RUN pip install mecab-python3
RUN pip install unidic-lite

WORKDIR /bot
COPY requirements.txt /bot/
RUN pip install -r requirements.txt
COPY . /bot
CMD python main.py
