from datetime import datetime, timedelta
from typing import Optional

import jwt
from fastapi import APIRouter, Request, Form, Depends, HTTPException
from jose import JWTError
from starlette import status
from starlette.responses import HTMLResponse, Response, RedirectResponse
from starlette.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import user_crud
from app.db.base import get_session
from app.models.user import User
from app.routers.auth_router import verify_password

router = APIRouter()
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

templates = Jinja2Templates(directory='templates')
@router.get('/login',response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse('login.html', {'request':request})

@router.post('/login')
async def login_user(
        response: Response,
        username: str = Form(...),
        password: str = Form(...),
        session: AsyncSession = Depends(get_session)
):
    user = await user_crud.get_user_by_username(session, username)

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Неверные данные')

    token_data = {
        'sub': user.username,
        'exp': datetime.utcnow() + timedelta(days=1)
    }

    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    response = RedirectResponse(url='/home',status_code=303)
    response.set_cookie(key='access_token',
                        value=token,
                        httponly=True,
                        path='/',
                        samesite='lax',
                        secure=False)
    return response




async def get_current_user_browser(
    request: Request,
    session: AsyncSession = Depends(get_session)
):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    credentials_exception = HTTPException(
        status_code=401,
        detail="Ошибка в пароле или логине",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await user_crud.get_user_by_username(session, username)
    if user is None:
        raise credentials_exception

    return user


@router.get("/logout")
def logout():
    response = RedirectResponse(url="/home", status_code=303)
    response.delete_cookie(key="access_token", path='/')
    return response
async def get_current_user_optional(
    request: Request,
    session: AsyncSession = Depends(get_session)
) -> Optional[User]:
    token = request.cookies.get("access_token")
    if not token:
        return None

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        user = await user_crud.get_user_by_username(session, username)
        return user
    except JWTError:
        return None
