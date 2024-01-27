from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel


class BearerResponse(BaseModel):
    token: str
    token_type: str


class BearerTransport:

    def __init__(self, path: str):
        self.scheme = OAuth2PasswordBearer(path)

    async def get_login_data(self, token: str) -> BearerResponse:
        return BearerResponse(token=token, token_type="Bearer")
