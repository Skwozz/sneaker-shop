from fastapi import APIRouter, Depends, HTTPException, status
import datetime
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError
from app.db.base import get_session
from app.schemas import user
from passlib.context import CryptContext
from app.crud import user_crud

router = APIRouter(prefix='/auth',tags=['auth'])
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = 'auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def crreate_access_token(data: dict, expire_delta: int | None = None):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(
        minutes=expire_delta or MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def authenticate_user(session: AsyncSession, username: str, password: str):
    user = await user_crud.get_user_by_username(session, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

@router.post('/token', response_model=user.Token)
async def login_with_access_token(
        session: AsyncSession = Depends(get_session),
        form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail='Ошибка в пароде или логине',
                            headers={"WWW-Authenticate": "Bearer"},)
    access_token = crreate_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

from fastapi import Request

async def get_current_user(
    request: Request,
    session: AsyncSession = Depends(get_session)
):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await user_crud.get_user_by_username(session, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


