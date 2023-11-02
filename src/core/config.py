"""App configuration"""
from typing import List

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings

from core.logger import set_logger


set_logger()


class AppSettings(BaseSettings):
    """Contains application settings"""
    app_title: str = 'URL Shortener'
    database_dsn: PostgresDsn
    black_list: List[str] = ['172.19.0.0',
                             ]

    class Config:
        """Application environment variables"""
        env_file = '.env.app'


app_settings = AppSettings()
 