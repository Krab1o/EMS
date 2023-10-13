from fastapi import FastAPI

from ems.adapters.http_api import controllers


def create_app(
        version: str,
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
    # include_router...
    return app
