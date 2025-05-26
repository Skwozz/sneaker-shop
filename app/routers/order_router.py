from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import order_crud
from app.db.base import get_session
from app.models.user import User
from app.routers.auth_router import get_current_user
from app.schemas import order

router = APIRouter(prefix="/order", tags=["order"])
@router.post("/create/", response_model=order.OrderBase)
async def create_order(
    order: order.OrderBase,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return await order_crud.create_order(session, order, current_user.id)
