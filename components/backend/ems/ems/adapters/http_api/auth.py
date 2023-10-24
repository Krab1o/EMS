from fastapi import HTTPException, status, Request

from ems_libs.security import jwt


async def get_auth_payload(
        request: Request
) -> dict | None:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    claims = jwt.decode_token(request.cookies.get('token', ''))
    if claims is None:
        raise credentials_exception
    return claims

