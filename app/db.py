from functools import lru_cache

import psycopg
from psycopg_pool import ConnectionPool, AsyncConnectionPool

from app.config import get_settings

settings = get_settings()

conninfo = f"user={settings.db_user} password={settings.db_password} host={settings.db_host} port={settings.db_port} dbname={settings.db_name}"


def get_conn():
    return psycopg.connect(conninfo=conninfo)


@lru_cache()
def get_pool():
    return ConnectionPool(conninfo=conninfo)


@lru_cache()
def get_async_pool():
    return AsyncConnectionPool(conninfo=conninfo)
