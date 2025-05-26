from fastapi import HTTPException
from sqlalchemy.orm import Session , selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.routers.auth_router import get_current_user
from app.models import cart_item as model_cart_item
from app.schemas import cart_item
async def get_cart_item(session: AsyncSession, user_id: int):
    result = await session.execute(select(model_cart_item.CartItem)
                    .options(selectinload(model_cart_item.CartItem.product))
                    .where(model_cart_item.CartItem.user_id == user_id))
    return result.scalars().all()


async def create_cart_item(session: AsyncSession, cart: cart_item.CartItemCreate, user_id:int):

    result = await session.execute(select(model_cart_item.CartItem)
                                   .where(model_cart_item.CartItem.user_id == user_id,
                                        model_cart_item.CartItem.product_id == cart.product_id))
    existinc_item = result.scalars().one_or_none()

    if existinc_item:
        existinc_item.quantity += cart.quantity
        await session.commit()
        await session.refresh(existinc_item)
        return existinc_item
    else:
        db_cart_item = model_cart_item.CartItem(
            product_id= cart.product_id,
            quantity = cart.quantity,
            user_id=user_id,
        )
        session.add(db_cart_item)
        await session.commit()
        await session.refresh(db_cart_item)
        return db_cart_item


async def delete_cart_item(session: AsyncSession, cart_item_id: int, user_id: int):
    result = await session.execute(select(model_cart_item.CartItem)
                                   .where(model_cart_item.CartItem.user_id==user_id,
                                          model_cart_item.CartItem.id==cart_item_id))
    cart_item = result.scalars().first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart Item not found")
    else:
        await session.delete(cart_item)
        await session.commit()
        return True
