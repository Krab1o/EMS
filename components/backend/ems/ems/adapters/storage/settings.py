from pydantic import Extra
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PUBLIC_DIR_PATH: str = '/var/www/ems/public'

    class Config:
        extra = Extra.ignore
        env_file = '.env'
        env_file_encoding = 'utf-8'
