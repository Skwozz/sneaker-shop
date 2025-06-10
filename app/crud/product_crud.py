from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.product import Product, Variant, SizeInfo
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate, VariantUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
async def get_product(session: AsyncSession):
    result = await session.execute(select(Product)
                            .options(selectinload(Product.variants)
                            .selectinload(Variant.sizes)))
    return result.scalars().all()

async def create_product(session: AsyncSession, product: ProductCreate):
    db_product = Product(
        name=product.name,
        brand=product.brand,
        style=product.style,
        description=product.description,
    )

    for var in product.variants:
        db_variant = Variant(
            price = float(var.price),
            image_url = var.image_url,
        )


        for size in var.sizes:
            db_size = SizeInfo(
                size=size.size,
                quantity=size.quantity
            )
            db_variant.sizes.append(db_size)
        db_product.variants.append(db_variant)

    session.add(db_product)
    await session.commit()
    await session.refresh(db_product)
    result = await session.execute(
        select(Product).
        options(selectinload(Product.variants)
                .selectinload(Variant.sizes))
                .where(Product.id == db_product.id)
    )
    product_with_variants = result.scalar_one()

    return product_with_variants


async  def get_product_by_id(
        session:AsyncSession,
        product_id: int,
):
    result = await session.execute(select(Product)
                                    .options(selectinload(Product.variants)
                                    .selectinload(Variant.sizes))
                                    .where(Product.id==product_id))
    return result.scalars().one_or_none()
async def delete_product(session: AsyncSession, product_id: int):
    result = await session.execute(select(Product).where(Product.id==product_id))
    product = result.scalars().first()
    if not product:
        raise HTTPException(status_code=404, detail="Product Item not found")
    else:
        await session.delete(product)
        await session.commit()
        return True

async def update_product(
        session: AsyncSession,
        product_id: int,
        product: ProductUpdate):
    result = await session.execute(select(Product).
                        options(selectinload(Product.variants)
                                .selectinload(Variant.sizes)).
                        where(Product.id == product_id))
    product_update = result.scalars().first()
    if not product_update:
        return None

    product_update.brand = product.brand
    product_update.style = product.style
    product_update.description = product.description

    await session.commit()
    await session.refresh(product_update)
    return product_update

async def update_variant_with_sizes(
        session: AsyncSession,
        variant_id: int,
        variant_data: VariantUpdate):
    result = await session.execute(select(Variant).
                        options(selectinload(Variant.sizes)).
                        where(Variant.id == variant_id))
    variant_result = result.scalars().first()
    if not variant_result:
        return None

    variant_result.price = variant_data.price
    variant_result.image_url = variant_data.image_url

    existing_sizes = {s.size: s for s in variant_result.sizes}
    incoming_sizes = {s.size: s for s in variant_data.sizes}

    for size, data in incoming_sizes.items():
        if size in existing_sizes:
            existing_sizes[size].quantity = data.quantity
        else:
            new_size = SizeInfo(
                variant_id=variant_id,
                size=size,
                quantity=data.quantity
            )
            session.add(new_size)
    for size in set(existing_sizes.keys()) - set(incoming_sizes.keys()):
        await session.delete(existing_sizes[size])
    await session.commit()
    await session.refresh(variant_result)
    return variant_result
