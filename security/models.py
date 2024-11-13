from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = 'Bearer'

class TokenData(BaseModel):
    username: str | None
    email: str
    expiration: str