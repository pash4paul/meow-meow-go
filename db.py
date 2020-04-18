import contextlib
from typing import List, Tuple

import psycopg2
from psycopg2.pool import ThreadedConnectionPool

import config
from logger import get_logger

LOGGER = get_logger(__name__)

connection_pool = ThreadedConnectionPool(
    minconn=config.DATABASE_WORKERS,
    maxconn=config.DATABASE_WORKERS,
    **config.DSN)


@contextlib.contextmanager
def get_connection() -> psycopg2.connect:
    conn = connection_pool.getconn()
    conn.set_isolation_level(0)
    yield conn
    connection_pool.putconn(conn)


def bulk_insert(items: List[Tuple]):
    inserted_rows = 0
    sql = 'INSERT INTO pages VALUES (%s, to_tsvector(%s))'
    with get_connection() as conn:
        cur = conn.cursor()
        for url, text in items:
            try:
                cur.execute(sql, (url, text))
                inserted_rows += 1
            except Exception as e:
                LOGGER.error('{} {} {}'.format(url, text[:50], str(e)))
    LOGGER.info(str(inserted_rows) + ' rows inserted')


__all__ = [bulk_insert]
