import sqlite3
import logging
from dataclasses import asdict
from typing import Generator
from logger import logger

from data_classes import( 
    class_from_args, FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork
    )


logger()

TABLES = {'film_work': FilmWork, 'genre': Genre, 
          'genre_film_work': GenreFilmWork, 
          'person': Person, 'person_film_work': PersonFilmWork}


class SQLiteExtractor:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        self.curs = self.conn.cursor()
        self.batch_size = 500

    def extract_movies(self) -> Generator:
        for table_name in TABLES:
            logging.info('Collecting from table {0}...'.format(table_name))
            result_list = []
            try:
                self.curs.execute("SELECT * FROM {0};".format(table_name))
            except Exception as e:
                logging.error(e)
            while True:
                data = self.curs.fetchmany(self.batch_size)
                if data:
                    for row in data:
                        cur_row = asdict(class_from_args(TABLES[table_name], row))
                        result_list.append(cur_row)
                else:
                    break
                # Calculating lenght is not reasonable performance-wise
                logging.info(f'Fetched around {self.batch_size} rows. Table name is {table_name}')
                # To understand from what table it is
                result_list.append(table_name)
                yield result_list
