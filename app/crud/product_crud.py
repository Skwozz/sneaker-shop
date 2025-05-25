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






