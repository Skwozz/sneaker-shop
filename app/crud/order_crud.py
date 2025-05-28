from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session, selectinload

from app.models.order_item_model import OrderItem
from app.models.order_model import Order
from app.schemas import order
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.cart_item import CartItem


async def get_order(session: AsyncSession, user_id: int):
    result = await session.execute(
        select(Order).options(selectinload(Order.order_items).selectinload(OrderItem.product))
        .where(Order.user_id == user_id,
               Order.is_deleted == False)
    )
    return result.scalars().all()

async def create_order_from_cart(session: AsyncSession, user_id):
    result = await session.execute(select(CartItem)
                                       .options(selectinload(CartItem.product))
                                       .where(CartItem.user_id == user_id))
    cart_items = result.scalars().all()

    if not cart_items:
        raise HTTPException(status_code=404, detail="Корзина пуста")
    new_order = Order(user_id=user_id, created_at=datetime.utcnow())
    session.add(new_order)
    await session.commit()
    await session.refresh(new_order)

    for item in cart_items:
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.product.price
        )
        session.add(order_item)

    for item in cart_items:
        await session.delete(item)

    await session.commit()
    result = await session.execute(
        select(Order)
        .options(
            selectinload(Order.order_items).selectinload(OrderItem.product)
        )
        .where(Order.id == new_order.id)
    )
    return result.scalar_one()

async def soft_delete_order(session: AsyncSession, user_id: int, order_id: int):
    result = await session.execute(select(Order)
                                   .where(Order.id == order_id,
                                          Order.user_id == user_id))
    order_del = result.scalars().first()
    if not order_del:
        return False
    order_del.is_deleted = True
    await session.commit()
    return True
