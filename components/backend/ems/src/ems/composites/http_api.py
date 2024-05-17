import aiohttp
from ems.adapters import database, http_api, log, storage
from ems.adapters.database import repositories
from ems.adapters.http_api import create_app
from ems.adapters.http_api.dependencies import Services, Sessions
from ems.adapters.http_api.dependencies import Settings as DepSettings
from ems.application import services
from ems_libs.security import jwt
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


class Settings:
    http_api = http_api.Settings()
    db = database.Settings()
    storage = storage.Settings()


class Logger:
    log.configure(Settings.http_api.LOGGING_CONFIG, Settings.db.LOGGING_CONFIG)


class DB:
    engine = create_async_engine(
        Settings.db.DATABASE_URL, echo=Settings.db.DATABASE_DEBUG
    )
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
    event_repository = repositories.EventRepository(
        async_session_maker=async_session_maker
    )
    user_repository = repositories.UserRepository(
        async_session_maker=async_session_maker
    )
    institution_repository = repositories.InstitutionRepository(
        async_session_maker=async_session_maker
    )
    event_type_repository = repositories.EventTypeRepository(
        async_session_maker=async_session_maker
    )
    user_voted_event_repository = repositories.UserVotedEventRepository(
        async_session_maker=async_session_maker
    )
    cover_repository = repositories.CoverRepository(
        async_session_maker=async_session_maker
    )
    club_repository = repositories.ClubRepository(
        async_session_maker=async_session_maker
    )
    user_favorite_club_repository = repositories.UserFavoriteClubRepository(
        async_session_maker=async_session_maker
    )
    place_repository = repositories.PlaceRepository(
        async_session_maker=async_session_maker
    )


class Storage:
    image_store = storage.ImageStore(config=Settings.storage)


class Application:
    event_service = services.EventService(
        event_repository=DB.event_repository,
        event_type_repository=DB.event_type_repository,
        user_voted_event_repository=DB.user_voted_event_repository,
        user_repository=DB.user_repository,
        cover_repository=DB.cover_repository,
        place_repository=DB.place_repository,
        image_store=Storage.image_store,
    )
    auth_service = services.AuthService(
        user_repository=DB.user_repository,
        institution_repository=DB.institution_repository,
    )
    event_type_service = services.EventTypeService(
        event_type_repository=DB.event_type_repository,
    )
    user_service = services.UserService(
        user_repository=DB.user_repository,
        institution_repository=DB.institution_repository,
    )
    club_service = services.ClubService(
        club_repository=DB.club_repository,
        user_repository=DB.user_repository,
        user_favorite_club_repository=DB.user_favorite_club_repository,
    )
    place_service = services.PlaceService(
        place_repository=DB.place_repository,
        institution_repository=DB.institution_repository,
    )


def init_security():
    jwt.set_secret_key(Settings.http_api.APP_SECRET_KEY)
    jwt.set_access_token_expires_minutes(
        Settings.http_api.APP_TOKEN_EXPIRE_MINUTES
    )


def init_services():
    Services.event = Application.event_service
    Services.auth = Application.auth_service
    Services.event_type = Application.event_type_service
    Services.user = Application.user_service
    Services.club = Application.club_service
    Services.place = Application.place_service
    Sessions.http_session = aiohttp.ClientSession()
    DepSettings.http_settings = Settings.http_api


def initial_app():
    init_security()
    init_services()


initial_app()
app = create_app(
    is_dev=Settings.http_api.APP_IS_DEV,
    is_debug=Settings.http_api.APP_IS_DEBUG,
    version=Settings.http_api.APP_VERSION,
    swagger_on=Settings.http_api.APP_SWAGGER_ON,
    title=Settings.http_api.APP_TITLE,
)
