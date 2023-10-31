from typing import Annotated

from fastapi import APIRouter, Response, Body, Depends, HTTPException, status

from ems.adapters.http_api.dependencies import get_auth_service
from ems.application import dto
from ems.application.services import AuthService
from ems.application.services.auth_service import LoginResult, RegistrationStatus
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
    match await security_service.login(body):
        case None, LoginResult.NOT_FOUND | LoginResult.WRONG_PASSWORD:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Invalid e-mail/password pair',
            )
        case user, LoginResult.OK:
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
    match await security_service.register_student(body):
        case None, RegistrationStatus.BAD_REQUEST | RegistrationStatus.INSTITUTION_NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Invalid field value',
            )
        case None, RegistrationStatus.EMAIL_TAKEN:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='E-mail is already in use',
            )
        case None, RegistrationStatus.UNEXPECTED_ERROR:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='An error occurred when tried to insert a new record'
            )
        case user, RegistrationStatus.OK:
            token = jwt.create_access_token(payload={
                'user_id': user.id,
                'role': user.role,
            })
            response.set_cookie(key='token', value=token)
            response.headers.append('Location', f'/users/{user.id}')
