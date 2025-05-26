from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
async def get_product(session: AsyncSession):
    result = await session.execute(select(Product))
    return result.scalars().all()

async def create_product(session: AsyncSession,
                          product: ProductCreate):
    db_product = Product(
        name = product.name,
        brand = product.brand,
        price = product.price,
        image_url = product.image_url,
        size = product.size,
    )
    session.add(db_product)
    await session.commit()
    await session.refresh(db_product)
    return db_product

async def delete_product(session: AsyncSession, product_id: int):
    result = await session.execute(select(Product).where(Product.id==product_id))
    product = result.scalars().first()
    if not product:
        raise HTTPException(status_code=404, detail="Product Item not found")
    else:
        await session.delete(product)
        await session.commit()
        return True





