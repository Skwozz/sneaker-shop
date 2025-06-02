from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from starlette import status

from app.db.base import get_session
from app.models.user import User
from app.routers.auth_router import get_current_user
from app.schemas.cart_item import CartItemRead, CartItemUpdate
from app.schemas import cart_item
from app.crud import cart_item_crud
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/cart", tags=["cart"])

@router.get("/get/", response_model=list[CartItemRead])
async def read_cart(
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
):
    return await cart_item_crud.get_cart_item(session, user_id=current_user.id)

@router.post("/create/", response_model= cart_item.CartItemCreate)
async def create_cart_item(
    cart_item: cart_item.CartItemCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await cart_item_crud.create_cart_item(session,
                                                 cart_item,
                                                 user_id=current_user.id)

@router.put('/cart_item_update/{item_id}',response_model= CartItemRead)
async def cart_item_update(
        item_id: int,
        cart_item_update: CartItemUpdate = Body(...),
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
):
    cart_item = await cart_item_crud.update_cart_item(
        session,
        cart_item_id=item_id,
        user_id=current_user.id,
        cart_item_update=cart_item_update)
    if not cart_item:
        raise HTTPException(status_code=404, detail='Товар в корзине не найден')
    return cart_item


@router.delete("/delete/{item_id}", status_code= status.HTTP_204_NO_CONTENT)
async def delete_cart_item(
    item_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    delete_result = await cart_item_crud.delete_cart_item(session, item_id, user_id=current_user.id)
    if not delete_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
    return delete_result









