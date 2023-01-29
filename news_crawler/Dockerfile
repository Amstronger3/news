FROM python:3.10.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python -m pip install --upgrade pip
RUN apt update & apt upgrade
#RUN mkdir -p /usr/news/news_crawler
RUN mkdir -p /usr/news/news_crawler/csv_news

COPY . /usr/news/news_crawler
WORKDIR /usr/news/news_crawler
RUN pip install -r requirements.txt

CMD ["python", "usa_today.py"]
