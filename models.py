from pydantic import BaseModel
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()

class User(Base):
    __tablename__ = "UserTable"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    username: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False, default="1234")
    is_active: Mapped[bool] = mapped_column(nullable=False, default=False)
    email: Mapped[str] = mapped_column(nullable=False, default="billy@dungeon.cum")

class UserResponse(BaseModel):
    username: str
    is_active: bool
    email: str

class UserInDb(UserResponse):
    password: str


class ErrorModel(BaseModel):
    status_code: int
    detail: str
    message:str
    addition: str = "2 + 2"