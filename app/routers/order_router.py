from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import order_crud
from app.db.base import get_session
from app.models.user import User
from app.routers.auth_router import get_current_user
from app.schemas.order import OrderBase

router = APIRouter(prefix="/order", tags=["order"])


@router.post("/create/", response_model=OrderBase)
async def create_orders(
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user)
):
    return await order_crud.create_order_from_cart(session, current_user.id)


@router.get("/get/", response_model=OrderBase)
async def read_order(
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
):
    return await order_crud.get_order(session, current_user.id)