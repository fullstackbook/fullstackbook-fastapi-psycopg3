from functools import lru_cache

from pydantic import BaseSettings

# uncomment to see psycopg.pool logs
# import logging
# logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
# logging.getLogger("psycopg.pool").setLevel(logging.INFO)


class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
