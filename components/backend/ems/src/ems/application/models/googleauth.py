from pydantic import BaseModel


class GoogleAuthResp(BaseModel):
    access_token: str
    id_token: str
    expires_in: int
    token_type: str
    scope: str
    refresh_token: str
