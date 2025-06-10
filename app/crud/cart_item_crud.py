from fastapi import HTTPException
from sqlalchemy.orm import Session , selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.product import Variant
from app.routers.auth_router import get_current_user
from app.models import cart_item as model_cart_item, product
from app.schemas import cart_item
from app.schemas.cart_item import CartItemUpdate


async def get_cart_item(session: AsyncSession, user_id: int):
    result = await session.execute(
        select(model_cart_item.CartItem)
        .options(
            selectinload(model_cart_item.CartItem.variant)
            .selectinload(Variant.sizes),
            selectinload(model_cart_item.CartItem.variant)
            .selectinload(Variant.product)
        )
        .where(model_cart_item.CartItem.user_id == user_id)
    )
    return result.scalars().all()



async def create_cart_item(session: AsyncSession, cart: cart_item.CartItemCreate, user_id: int):

    result = await session.execute(
        select(product.Variant)
        .options(selectinload(product.Variant.sizes))
        .where(product.Variant.id == cart.variant_id)
    )
    variant = result.scalar_one_or_none()

    if not variant:
        raise HTTPException(status_code=404, detail="Вариант товара не найден")

    matched_size = None
    for s in variant.sizes:
        if s.size == cart.size:
            matched_size = s
            break

    if not matched_size:
        raise HTTPException(
            status_code=404,
            detail=f"Размер {cart.size} не найден для данного варианта"
        )

    result = await session.execute(
        select(model_cart_item.CartItem).where(
            model_cart_item.CartItem.user_id == user_id,
            model_cart_item.CartItem.variant_id == cart.variant_id,
            model_cart_item.CartItem.size == cart.size
        )
    )
    existing_item = result.scalar_one_or_none()

    if existing_item:
        new_quantity = existing_item.quantity + cart.quantity


        if new_quantity > matched_size.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"На складе только {matched_size.quantity} шт"
            )
        existing_item.quantity = new_quantity

        await session.commit()
        await session.refresh(existing_item)
        return existing_item

    if cart.quantity > matched_size.quantity:
        raise HTTPException(
            status_code=400,
            detail=f"На складе только {matched_size.quantity} шт размера {cart.size}"
        )

    db_cart_item = model_cart_item.CartItem(
        variant_id=cart.variant_id,
        size= cart.size,
        quantity=cart.quantity,
        user_id=user_id,
    )
    session.add(db_cart_item)
    await session.commit()
    await session.refresh(db_cart_item)
    return db_cart_item
async def update_cart_item(
        session: AsyncSession,
        cart_item_id: int,
        user_id: int,
        cart_item_update: CartItemUpdate):
    result = await session.execute(select(model_cart_item.CartItem).
                        options(selectinload(model_cart_item.CartItem.variant)).
                        where(model_cart_item.CartItem.id == cart_item_id,
                        model_cart_item.CartItem.user_id == user_id))
    cart_item = result.scalars().first()
    if not cart_item:
        return None

    cart_item.quantity = cart_item_update.quantity
    await session.commit()
    await session.refresh(cart_item)
    return cart_item




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
