import logging
from psycopg2.extensions import connection
from logger import logger

logger()

class PostgresSaver:
    def __init__(self, pg_conn: connection):
        self.conn = pg_conn
        self.curs = self.conn.cursor()

    def save_all_data(self, data: list) -> None:
        table_name = data.pop()
        keys = data[0].keys()
        columns = ', '.join(keys)
        args = ', '.join(['%s' for key in keys])
        for row in data:
            row_values = tuple(row.values())
            try:
                self.curs.execute(f"""
                    INSERT INTO content.{table_name} ({columns})
                    VALUES ({args})
                    ON CONFLICT (id) DO NOTHING
                """, row_values)
            except Exception as e:
                logging.error(e)
        logging.info(f'Inserted into {table_name}.')
