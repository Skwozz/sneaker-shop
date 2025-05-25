from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.base import get_session
from app.schemas.product import ProductCreate, ProductRead
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
    return await product_crud.get_product(session,)