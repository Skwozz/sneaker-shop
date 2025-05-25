from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_session
from app.schemas import user
from app.models.user import User
from app.crud import user_crud
from app.routers.auth import get_current_user
router = APIRouter(prefix='/user',tags=['user'])

@router.post("/register/", response_model=user.UserRead)
async def register_user(user: user.UserCreate, session: AsyncSession = Depends(get_session)):
    existing = await user_crud.get_user_by_username(session, user.username)
    if existing:
        raise HTTPException(status_code=400, detail="Пользователь с таким именем уже существует")
    return await user_crud.create_user(session, user)

@router.get("/me")
async def read_me(current_user: User = Depends(get_current_user)):
    return current_user