from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.crud.product_crud import update_product
from app.db.base import get_session
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate, VariantUpdate
from app.crud import product_crud
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/products", tags=["products"])

@router.post('/create', response_model= ProductRead)
async def create_product(
        product: ProductCreate,
        session: AsyncSession = Depends(get_session)
):
    return await product_crud.create_product(session, product)


@router.get('/get', response_model=list[ProductRead])
async def get_products(
        session: AsyncSession = Depends(get_session)
):
    return await product_crud.get_product(session)

@router.get('/get/{prodict_id}', response_model=ProductRead)
async def get_products_by_id(
        product_id: int,
        session: AsyncSession = Depends(get_session),

):
    return await product_crud.get_product_by_id(session,product_id)
@router.delete('/delete/{id}', status_code= status.HTTP_204_NO_CONTENT)
async def delete_product(
        id: int,
        session: AsyncSession = Depends(get_session)
):
    delete_result = await product_crud.delete_product(session, id)
    if not delete_result:
        raise HTTPException(status_code=404, detail="Product not found")
    return  delete_result

@router.put('/product/{product_id}',response_model= ProductUpdate)
async def cart_item_update(
        product_id: int,
        product_update: ProductUpdate,
        session: AsyncSession = Depends(get_session)
):
    product = await product_crud.update_product(
        session,
        product_id= product_id,
        product=product_update)

    return product

@router.put('/variant/{variant_id}',response_model= VariantUpdate)
async def variant_update(
        variant_id: int,
        variant: VariantUpdate,
        session: AsyncSession = Depends(get_session)
):
    variant_up = await product_crud.update_variant_with_sizes(
        session,
        variant_id= variant_id,
        variant_data=variant)

    return variant_up