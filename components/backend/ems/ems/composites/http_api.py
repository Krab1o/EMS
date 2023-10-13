from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from ems_libs.security import jwt_strategy

from ems.adapters import database, http_api, log
from ems.adapters.database import repositories
from ems.adapters.http_api import create_app
from ems.adapters.http_api.dependencies import Services
from ems.application import services


class Settings:
    http_api = http_api.Settings()
    db = database.Settings()
    
    
class Logger: 
    log.configure(Settings.http_api.LOGGING_CONFIG, Settings.db.LOGGING_CONFIG)
    
    
class DB:
    engine = create_async_engine(Settings.db.DATABASE_URL, echo=Settings.db.DATABASE_DEBUG)
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
    # repositories...


class Application:
    # create services...
    pass


def init_security():
    jwt_strategy.set_secret_key(Settings.http_api.APP_SECRET_KEY)
    jwt_strategy.set_access_token_expires_minutes(Settings.http_api.APP_TOKEN_EXPIRE_MINUTES)


def init_services():
    # put services in framework layer
    pass


def initial_app():
    init_security()
    init_services()

    
initial_app()
app = create_app(
    is_debug=Settings.http_api.APP_IS_DEBUG,
    version=Settings.http_api.APP_VERSION,
    swagger_on=Settings.http_api.APP_SWAGGER_ON,
    title=Settings.http_api.APP_TITLE
)
