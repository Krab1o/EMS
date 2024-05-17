from pydantic import BaseModel


class TokenResp(BaseModel):
    token: str
