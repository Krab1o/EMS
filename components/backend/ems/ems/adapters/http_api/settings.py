from pydantic import Extra
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_IS_DEBUG: bool = False
    APP_VERSION: str = '0.0.1'
    APP_SWAGGER_ON: bool = False
    APP_TITLE: str = 'EMS'
    APP_LOGGING_LEVEL: str = 'INFO'

    # SECURITY 

    # openssl rand -hex 32
    APP_SECRET_KEY: str = '52f2e5c5beaeca1b342d4eca7c40bacd6ab7b641e370a12acd98dccf5c59682c'
    # один день
    APP_TOKEN_EXPIRE_MINUTES: int = 1440
    
    @property
    def LOGGING_CONFIG(self):
        return {
            'loggers': {
                'gunicorn': {
                    'handlers': ['default'],
                    'level': self.APP_LOGGING_LEVEL,
                    'propagate': False
                },
                'uvicorn': {
                    'handlers': ['default'],
                    'level': self.APP_LOGGING_LEVEL,
                    'propagate': False
                },
            }
        }

    class Config:
        extra = Extra.ignore
        env_file = '.env'
        env_file_encoding = 'utf-8'
    
    