from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

SECRET_KEY = "iwanttobreakfreefromyourliesyouaresoselfsatisfiedidontneedyou"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRES_SECONDS = 120
pwd_encrypt = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="MyToken")

