from typing import Annotated

from ems.application.enum import UserRole
from ems.application.services import AuthService
from ems_libs.security import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

jwt_scheme = HTTPBearer(scheme_name="JWT Bearer")


async def get_auth_payload(
    token: Annotated[HTTPAuthorizationCredentials, Depends(jwt_scheme)],
) -> dict | None:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    claims = jwt.decode_token(token.credentials)
    if claims is None:
        raise credentials_exception
    return claims


async def get_user_role(
    auth_service: AuthService, user_id: int
) -> UserRole | None:
    return await auth_service.get_user_role(user_id)
