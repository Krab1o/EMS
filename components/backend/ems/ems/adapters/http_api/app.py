from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ems.adapters.http_api import controllers


def create_app(
        version: str,
        is_dev: bool = False,
        is_debug: bool = False,
        swagger_on: bool = False,
        title: str = 'noname'
) -> FastAPI:
    """ Собирает основное приложение """
    app = FastAPI(
        title=title,
        debug=is_debug,
        version=version,
        docs_url='/docs' if swagger_on else None,
        redoc_url='/redoc' if swagger_on else None,
    )

    app.include_router(controllers.event_router)
    app.include_router(controllers.auth_router)
    app.include_router(controllers.event_type_router)

    if is_dev:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_methods=['*'],
            allow_headers=['*'],
        )

    return app
