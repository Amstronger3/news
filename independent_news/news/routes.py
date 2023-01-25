from news import app
from db_connection import DB
from config import requirements_for_news_db


@app.route("/", methods=['GET'])
def get_current_day_news():
    db = DB(requirements_for_news_db)
    request = 'SELECT * FROM articles WHERE CAST(published_date AS DATE) = CURRENT_DATE;'
    current_day_news = db.make_request(request).fetchall()
    db.close_connection()
    response = []
    for news in current_day_news:
        news_id, scrap_date, published_date, source_link, source_name, author, text_article, header_original, header_english, country = news
        news_object = {
            'id': news_id,
            'scrap_date': scrap_date,
            'published_date': published_date,
            'source_link': source_link,
            'source_name': source_name,
            'author': author,
            'text_article': text_article,
            'header_original': header_original,
            'header_english': header_english,
            'country': country
        }
        response.append(news_object)

    return response
