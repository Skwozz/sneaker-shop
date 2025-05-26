from fastapi import HTTPException
from sqlalchemy.orm import Session, selectinload

from app.models.order_item_model import OrderItem
from app.models.order_model import Order
from app.schemas import order
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.cart_item import CartItem
from app.schemas import order_item


async def create_order(session: AsyncSession,
                       order: order_item.OrderItemCreate,
                       user_id: int):
    result = await session.execute(select(CartItem)
                                       .options(selectinload(CartItem.product))
                                       .where(CartItem.user_id == user_id))
    cart_items = result.scalars().all()

    if not cart_items:
        raise HTTPException(status_code=404, detail="Корзина пуста")
    new_order = Order(user_id=user_id)
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
    await session.refresh(new_order)
    return new_order