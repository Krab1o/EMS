from typing import Annotated

from fastapi import APIRouter, Response, Body, Depends, HTTPException, status

from ems.adapters.http_api.dependencies import get_auth_service
from ems.application import dto
from ems.application.services import AuthService
from ems.application.services.auth_service import LoginResult, RegistrationResult
from ems_libs.security import jwt

router = APIRouter(
    prefix='/auth',
    tags=['Авторизация']
)


@router.post(
    path='/login',
    responses={
        200: {'description': 'Пользователь авторизован.'},
        404: {'description': 'Пользователь не найден или неверный пароль.'},
    },
)
async def login(
        security_service: Annotated[AuthService, Depends(get_auth_service)],
        response: Response,
        body: dto.LoginRequest = Body(),
):
    user, result = await security_service.login(body)

    if result == LoginResult.NOT_FOUND or result == LoginResult.WRONG_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Invalid pair email/password',
        )

    token = jwt.create_access_token(payload={
        'user_id': user.id,
        'role': user.role,
    })
    response.set_cookie(key='token', value=token)


@router.post(
    path='/register',
    status_code=201,
    responses={
        201: {'description': 'Пользователь зарегистрирован.'},
        400: {'description': 'Формат некоторых полей неверный или институт с таким ID не найден.'},
        409: {'description': 'E-mail уже используется.'}
    },
)
async def register(
        security_service: Annotated[AuthService, Depends(get_auth_service)],
        response: Response,
        body: dto.UserCreateRequest = Body()
):
    user, result = await security_service.register_student(body)

    if result == RegistrationResult.BAD_REQUEST or result == RegistrationResult.INSTITUTION_NOT_FOUND:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid field value',
        )
    elif result == RegistrationResult.EMAIL_TAKEN:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='E-mail is already in use',
        )

    token = jwt.create_access_token(payload={
        'user_id': user.id,
        'role': user.role,
    })
    response.set_cookie(key='token', value=token)
    response.status_code = status.HTTP_201_CREATED
