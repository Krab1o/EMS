from pydantic import Extra
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_NAME: str = 'dev_ems'
    DATABASE_HOST: str = 'localhost'
    DATABASE_PORT: int = 5430
    DATABASE_USER: str = 'postgres'
    DATABASE_PASS: str = 'postgres'
    DATABASE_DEBUG: bool = False

    ALEMBIC_SCRIPT_LOCATION: str = 'ems.adapters.database:alembic'
    ALEMBIC_VERSION_LOCATIONS: str = 'ems.adapters.database:migrations'
    ALEMBIC_MIGRATION_FILENAME_TEMPLATE: str = (
        '%%(year)d_'
        '%%(month).2d_'
        '%%(day).2d_'
        '%%(hour).2d_'
        '%%(minute).2d_'
        '%%(second).2d_'
        '%%(slug)s'
    )
    LOGGING_LEVEL: str = 'INFO'
    SA_LOGS: bool = False

    @property
    def LOGGING_CONFIG(self):
        config = {
            'loggers': {
                'alembic': {
                    'handlers': ['default'],
                    'level': self.LOGGING_LEVEL,
                    'propagate': False
                }
            }
        }
        if self.DATABASE_DEBUG:
            config['loggers'].update(
                {
                    'sqlalchemy': {
                        'handlers': ['default'],
                        'level': self.LOGGING_LEVEL,
                        'propagate': False
                    },
                    'sqlalchemy.engine': {
                        'handlers': ['default'],
                        'level': self.LOGGING_LEVEL,
                        'propagate': False
                    },
                    'sqlalchemy.engine.Engine': {
                        'handlers': ['default'],
                        'level': self.LOGGING_LEVEL,
                        'propagate': False
                    }
                }
            )
        return config

    @property
    def DATABASE_URL(self):
        url = 'postgresql+asyncpg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'

        return url.format(
            db_user=self.DATABASE_USER,
            db_pass=self.DATABASE_PASS,
            db_host=self.DATABASE_HOST,
            db_name=self.DATABASE_NAME,
            db_port=self.DATABASE_PORT,
        )

    class Config:
        extra = Extra.ignore
        env_file = '.env'
        env_file_encoding = 'utf-8'
