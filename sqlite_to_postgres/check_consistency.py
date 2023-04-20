import sqlite3
from psycopg2.extensions import connection as pg_connection
from dataclasses import asdict

from data_classes import( 
    class_from_args, FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork
    )


TABLES = {'film_work': FilmWork, 'genre': Genre, 
          'genre_film_work': GenreFilmWork, 
          'person': Person, 'person_film_work': PersonFilmWork}

class Tests:
    def __init__(self, sqlite_conn: sqlite3.Connection, pg_conn: pg_connection) -> None:
        self.sqlite_curs = sqlite_conn.cursor()
        self.pg_curs = pg_conn.cursor()

    def count_rows(self, table_name: str) -> None:
        """Compare rows count from sqlite and pg DBs"""
        self.sqlite_curs.execute("""
            SELECT COUNT(*) FROM {0}
        """.format(table_name))
        sqlite_count = tuple(self.sqlite_curs.fetchone())
        print(sqlite_count)
        self.pg_curs.execute("""
            SELECT COUNT(*) FROM content.{0}
        """.format(table_name))
        pg_count = tuple(self.pg_curs.fetchone())
        assert sqlite_count == pg_count
        
    def check_content(self, table_name: str) -> None:
        """Compare contents from sqlite and pg DBs"""
        self.sqlite_curs.execute("""
            SELECT * FROM {0}
            ORDER BY id DESC;
        """.format(table_name))
        sqlite_row = self.sqlite_curs.fetchone()
        self.pg_curs.execute("""
            SELECT * FROM content.{0}
            ORDER BY id DESC;
        """.format(table_name))
        pg_row = self.pg_curs.fetchone()
        # transforming them into dataclass to compare datetime correctly
        sqlite_dc = asdict(class_from_args(TABLES[table_name], sqlite_row))
        pg_dc = asdict(class_from_args(TABLES[table_name], pg_row))
        assert sqlite_dc == pg_dc
