import logging
from typing import Annotated

import aiohttp
from ems.adapters.http_api.dependencies import (
    get_auth_service,
    get_http_session,
    get_http_settings,
    get_user_service,
)
from ems.adapters.http_api.settings import Settings
from ems.application import dto
from ems.application.models.googleauth import GoogleAuthResp
from ems.application.models.googleuser import GoogleUserResp
from ems.application.services.auth_service import AuthService
from ems.application.services.user_service import UserService
from ems_libs.security import jwt
from fastapi import APIRouter, Depends, HTTPException, Query

logger = logging.getLogger("ems")
router = APIRouter(prefix="/googleauth", tags=["Google OAuth2"])


@router.get(
    "",
    responses={
        200: {
            "description": "Успех",
        },
        502: {
            "description": "Ошибка при обращении к Google Auth API"
        },
    },
)
async def authorize_with_code(
    code: Annotated[str, Query()],
    http_session: Annotated[aiohttp.ClientSession, Depends(get_http_session)],
    user_service: Annotated[UserService, Depends(get_user_service)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    settings: Annotated[Settings, Depends(get_http_settings)],
):
    logger.debug("Received auth code. Trying to authorize using Google Auth API")
    async with http_session.post(
        "https://oauth2.googleapis.com/token",
        data={
            "code": code,
            # Do we need this?
            # "redirect_uri": "",
            "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
            "client_secret": settings.GOOGLE_OAUTH_SECRET,
            "scope": "",
            "grant_type": "authorization_code",
        }
    ) as resp:
        if resp.status == 200:
            logger.debug("Successful response from the Google Auth API")
            json_resp = await resp.json()
            auth = GoogleAuthResp.model_validate(json_resp)
            logger.debug(f"Parsed JSON response into object: {auth}")
        else:
            logger.error(f"Google Auth API request failed ({resp.status}):\n{resp}")
            raise HTTPException(
                502,
                detail="Google Auth API request has failed"
            )
    
    logger.debug("Retrieving user email from the Google User API")
    async with http_session.get(
        "https://oauth2.googleapis.com/userinfo/v2/me",
        headers={
            "Authorization": "Bearer " + auth.access_token,
        }
    ) as resp:
        if resp.status == 200:
            logger.debug("Successful response from the Google User API")
            json_resp = await resp.json()
            g_user = GoogleUserResp.model_validate(json_resp)
            logger.debug(f"Prased JSON response into object: {g_user}")
        else:
            logger.error(f"Google User API request failed ({resp.status}):\n{resp}")
            raise HTTPException(
                502,
                detail="Google User API request has failed"
            )
    
    logger.debug("Checking if email is not already taken")
    db_user = await user_service.get_by_email(g_user.email)
    if db_user is not None:
        logger.debug("Email is already in use, authorizing user")
        token = jwt.create_access_token(
            payload={
                "user_id": db_user.id,
            }
        )
        return {"token": token}

    reg_req = dto.UserCreateRequest(
        last_name="Google",
        first_name="Пользователь",
        email=g_user.email,
        password="",
    )
    db_user, _ = await auth_service.register_student(reg_req)
    token = jwt.create_access_token(
        payload={
            "user_id": db_user.id,
        }
    )
    return {"token": token}
