from typing import Annotated

from fastapi import HTTPException, status, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from ems_libs.security import jwt

jwt_scheme = HTTPBearer(scheme_name='JWT Bearer')


async def get_auth_payload(
        token: Annotated[HTTPAuthorizationCredentials, Depends(jwt_scheme)]
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
