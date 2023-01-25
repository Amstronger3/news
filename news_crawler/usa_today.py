import datetime
import os

import pandas as pd

from utils import config_news
from utils.connection_db import DB as db
from utils.scraper_tools import Scraper

SOURCE_NAME = 'USA Today'
URL = config_news.source_urls[SOURCE_NAME]
COUNTRY = 'USA'
file_name = os.path.basename(__file__).split('.')[0]
PATH = f'{os.getcwd()}/csv_news'


def scrap_news() -> pd.DataFrame:
    """
    Scrap news data
    :return: Frame with scraped data
    """

    news_data = pd.DataFrame(
        columns=['scrap_date',
                 'published_date',
                 'source_link',
                 'source_name',
                 'author',
                 'text_article',
                 'header_original',
                 'header_english',
                 'country'])

    filtered_news_by_data_index = list(
        filter(lambda x: x.has_attr('data-index'), Scraper(URL).get_bs_response().find_all('a')))

    for i in filtered_news_by_data_index:
        if i.get('href').startswith('/'):
            scrap_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            published_date = datetime.datetime.strptime(i.find(id='storyTimestamp').get('publishdate'),
                                                        '%Y-%m-%dT%H:%M:%SZ') \
                if i.find(id='storyTimestamp') else ''

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

            parsed_news = pd.DataFrame.from_dict({
                'scrap_date': [scrap_date],
                'published_date': [published_date],
                'source_link': [source_link],
                'source_name': [source_name],
                'author': [author],
                'text_article': [text_article],
                'header_original': [header_original],
                'header_english': [header_english],
                'country': [country],
            })

            news_data = pd.concat([news_data, parsed_news], ignore_index=True)

    news_data = news_data.astype({'scrap_date': 'datetime64[ns]',
                                  'published_date': 'datetime64[ns]',
                                  'source_link': str,
                                  'source_name': str,
                                  'author': str,
                                  'text_article': str,
                                  'header_original': str,
                                  'header_english': str,
                                  'country': str
                                  })
    print(news_data)
    return news_data


def save_to_csv(data):
    # Pay attention that parameter header=False is required. Else loading to DB will be failed.
    data.to_csv(f'{PATH}/{file_name}_news.csv', index=False, header=False)


def load_to_db():
    connection = db(config_news.requirements_for_news_db)
    query = f"""
    COPY articles (scrap_date, published_date, source_link, source_name, author, text_article, header_original,
                    header_english, country)
    FROM '{PATH}/{file_name}_news.csv' DELIMITERS ',' CSV;
    """
    connection.make_request(query)
    connection.drop_duplicates()
    connection.close_connection()


def main():
    scrap_data = scrap_news()
    save_to_csv(scrap_data)
    load_to_db()


if __name__ == '__main__':
    main()
