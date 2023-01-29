import psycopg2


class DB:
    """
    This class allow work with DB tables.

    open_connection() - open connect to DB
    make_request() - make request and commit to DB
    close_connection() - close connect to DB
    drop_duplicate() - delete duplicates from DB
    """

    def __init__(self, requirements):
        self.connection = psycopg2.connect(requirements)
        self.cursor = self.connection.cursor()

    def insert_many(self, query, data):
        self.cursor.executemany(query, data)
        return self.cursor

    def make_request(self, request):
        self.cursor.execute(request)
        self.connection.commit()
        return self.cursor

    def close_connection(self):
        self.connection.close()

    def drop_duplicates(self):
        self.make_request('''
            DELETE FROM articles AS a USING articles AS b 
            WHERE a.scrap_date < b.scrap_date AND a.source_link = b.source_link;
                        ''')
