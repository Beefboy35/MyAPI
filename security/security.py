import datetime
from datetime import timedelta

from fastapi import Depends, HTTPException
import jwt
from fastapi.encoders import jsonable_encoder

from starlette import status
from security.config import SECRET_KEY, ALGORITHM, oauth2_scheme, pwd_encrypt
from routes.localization import translate_message
from security.models import TokenData


def create_jwt_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.datetime.now(tz=datetime.UTC) + (
        expires_delta if expires_delta else timedelta(seconds=200)
    )
    expire = jsonable_encoder(expire)
    to_encode.update({"expiration": expire})
    return jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=translate_message("Could not validate credentials", "en"),
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("sub")
        email: str = payload.get("email")
        expiration: str = payload.get("expiration")
        if (username, email, expiration) is None:
            raise credentials_exception
        return TokenData(username=username, email=email, expiration=expiration)
    except Exception as e:
        print(e)


def get_password_hashed(password):
    return pwd_encrypt.hash(password)


def verify_password(plain, hashed):
    return pwd_encrypt.verify(plain, hashed)



