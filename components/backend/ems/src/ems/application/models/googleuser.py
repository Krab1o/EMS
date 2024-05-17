from typing import Optional

from pydantic import BaseModel


class GoogleUserResp(BaseModel):
    picture: Optional[str]
    verified_email: bool
    id: str
    email: str
