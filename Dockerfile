FROM python:3.9

RUN pip install -U pip

RUN apt-get clean \
  && apt-get update \
  && apt-get install -y mecab \
  && apt-get install -y mecab-ipadic \
  && apt-get install -y libmecab-dev \
  && apt-get install -y mecab-ipadic-utf8 \
  && apt-get install -y swig \
  && apt-get install -y tesseract-ocr

# 任意の場所に学習データを配置
RUN mkdir -p /usr/share/tesseract-ocr/4.00/tessdata
COPY ./jpn.traineddata /usr/share/tesseract-ocr/4.00/tessdata/jpn.traineddata

WORKDIR /bot
COPY requirements.txt /bot/
RUN pip install -r requirements.txt
COPY . /bot
CMD python main.py
