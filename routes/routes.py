from datetime import timedelta

from fastapi import Depends, APIRouter, HTTPException

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_localization import TranslateJsonResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status


from Exception_handling.classes import InvalidUserException, InvalidDataException, UserNotFound
from db.connection import get_db
from models import UserInDb, UserResponse, User
from routes.localization import translate_message
from security.config import pwd_encrypt, ACCESS_TOKEN_EXPIRES_SECONDS
from security.models import Token, TokenData
from security.security import get_password_hashed, create_jwt_token, get_current_user

app = APIRouter()





@app.post("/register", response_model=UserResponse, response_class=TranslateJsonResponse)
async def login(user: UserInDb, db: AsyncSession = Depends(get_db)):
    existing_user = await  db.execute(select(User).filter(User.username == user.username))
    existing_user = existing_user.scalars().first()
    if existing_user:
        raise InvalidUserException(
            detail=translate_message("User already exists.", "en"),
            message="Try it again later"
        )
    existing_email = await db.execute(select(User).filter(User.email == user.email))
    existing_email = existing_email.scalars().first()
    if existing_email:
            raise InvalidDataException(
            detail=translate_message("Email already exists.", "ru"),
            message="Try it again later"
        )
    if "@" not in user.email:
        raise InvalidDataException(
            detail=translate_message("Invalid email address.", "ru"),
            message="Make sure there is the @ sign in your address"
        )

    unit = User(
        username=user.username,
        hashed_password=get_password_hashed(user.password),
        is_active=user.is_active,
        email=user.email
    )
    db.add(unit)
    await db.commit()
    await db.refresh(unit)
    return UserResponse(username=user.username, is_active=user.is_active, email=user.email)

@app.get("/user/{user}", response_model=UserResponse, response_class=TranslateJsonResponse)
async def login(user: str, db: AsyncSession = Depends(get_db)):
    query = await db.execute(select(User).filter(User.username == user))
    query = query.scalars().first()
    if not query:
        raise UserNotFound(user)
    return query


@app.put("/update_user/{user}", response_model=UserResponse)
async def update_user(change: UserInDb, user: str, db: AsyncSession = Depends(get_db)):
    query = await db.execute(select(User).filter(User.username == user))
    query = query.scalars().first()
    if not query:
        raise UserNotFound(user)
    query.username = change.username
    query.email = change.email
    query.is_active = change.is_active
    query.hashed_password = get_password_hashed(change.password)
    await db.commit()
    await db.refresh(query)
    return query

@app.delete("/delete_user/{user}")
async def delete_user(user: str, db: AsyncSession = Depends(get_db)):
    query = await db.execute(select(User).filter(User.username == user))
    query = query.scalars().first()
    if not query:
        raise UserNotFound(user)
    await db.delete(query)
    await db.commit()
    return {"message": "successfully deleted"}

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.username == form_data.username))
    result = result.scalars().first()
    if not result or not pwd_encrypt.verify(form_data.password, result.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=translate_message("Incorrect username or password", "ru"),
            headers= {"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(seconds=ACCESS_TOKEN_EXPIRES_SECONDS)
    token = create_jwt_token({"sub": result.username, "email": result.email}, access_token_expires)
    return Token(access_token=token, token_type="Bearer")


@app.get("/users/me", response_model=UserResponse)
async def read_my_stuff(current_user: TokenData = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    query = await db.execute(select(User).filter(User.username == current_user.username))
    query = query.scalars().first()
    return UserResponse(username=query.username, is_active=query.is_active, email=query.email)
