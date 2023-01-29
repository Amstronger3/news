import datetime
import os
import time

from utils import config_news
from utils.connection_db import DB as db
from utils.scraper_tools import Scraper

SOURCE_NAME = 'USA Today'
URL = config_news.source_urls[SOURCE_NAME]
COUNTRY = 'USA'
file_name = os.path.basename(__file__).split('.')[0]
PATH = f'{os.getcwd()}/csv_news'


def scrap_news() -> list:
    """
    Scrap news data
    :return: Frame with scraped data
    """
    news_data = list()

    filtered_news_by_data_index = list(
        filter(lambda x: x.has_attr('data-index'), Scraper(URL).get_bs_response().find_all('a')))

    for i in filtered_news_by_data_index:
        if i.get('href').startswith('/'):
            scrap_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            published_date = datetime.datetime.strptime(i.find(id='storyTimestamp').get('publishdate'),
                                                        '%Y-%m-%dT%H:%M:%SZ') \
                if i.find(id='storyTimestamp') else None

            source_link = f"{URL}{i.get('href')}"
            source_name = SOURCE_NAME
            author = ''
            text_article = ''
            header_original = ' '.join((i.find(class_='p1-title-spacer').text
                                        if i.find(class_='p1-title-spacer') else i.find(
                class_='display-6 p13-title').text
            if i.find(class_='display-6 p13-title') else '').split())

            header_english = ''
            country = COUNTRY

            news_data.append((scrap_date,
                              published_date,
                              source_link,
                              source_name,
                              author,
                              text_article,
                              header_original,
                              header_english,
                              country))

    print(news_data)
    return news_data


def load_to_db(scraped_data):
    connection = db(config_news.requirements_for_news_db)
    query = f"""
    INSERT INTO articles (scrap_date, published_date, source_link, source_name, author, text_article, header_original,
                    header_english, country) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    connection.insert_many(query, scraped_data)
    connection.drop_duplicates()
    connection.close_connection()


def main():
    scraped_data = scrap_news()
    load_to_db(scraped_data)


if __name__ == '__main__':
    while True:
        main()
        time.sleep(600)
