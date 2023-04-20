import os
from contextlib import contextmanager, closing

import sqlite3
import psycopg2
import logging
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from dotenv import load_dotenv
from logger import logger

from copy_sqlite1 import SQLiteExtractor
from load_psql1 import PostgresSaver


logger()

load_dotenv()

dsl = {'dbname': os.environ.get('DB_NAME'), 'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'), 'host': '127.0.0.1', 'port': 5432}

@contextmanager
def open_sqlite(connection: sqlite3.Connection) -> None:
    try:
        yield connection
    finally:
        connection.close()

def dict_factory(curs, row):
    fields = [column[0] for column in curs.description]
    return {key: value for key, value in zip(fields, row)}

def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection) -> None:
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_extractor = SQLiteExtractor(connection)
    data_generator = sqlite_extractor.extract_movies()
    for row in data_generator:
        postgres_saver.save_all_data(row)

if __name__ == '__main__':
    with open_sqlite(sqlite3.connect(os.environ.get('SQLITE_PATH'))) as sqlite_conn, \
    closing(psycopg2.connect(**dsl, cursor_factory=DictCursor)) as pg_conn:
        logging.info('Launching process...')
        sqlite_conn.row_factory = dict_factory
        load_from_sqlite(sqlite_conn, pg_conn)
