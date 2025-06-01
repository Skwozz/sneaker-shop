from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from datetime import datetime, timedelta
from app.crud import product_crud
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_session
from app.models.user import User
from app.routers.auth_router import get_current_user
from app.crud.cart_item_crud import create_cart_item, get_cart_item, delete_cart_item
from app.routers.login_router import get_current_user_browser
from app.schemas.cart_item import CartItemCreate

router = APIRouter()
templates = Jinja2Templates(directory='templates')

@router.get('/home', response_class=HTMLResponse)
async def home(request: Request,
               session: AsyncSession = Depends(get_session)):
    products = await product_crud.get_product(session)
    return templates.TemplateResponse('index.html',
                                      {'request': request,
                                        'products':products
                                                     })

@router.post('/add-to-cart/')
async def add_to_cart(
        product_id: int = Form(...),
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user_browser)
):
    cart_data = CartItemCreate(product_id=product_id, quantity=1)
    await create_cart_item(session, cart_data, current_user.id)
    return  RedirectResponse(url='/home',status_code=303)


@router.get('/cart/', response_class=HTMLResponse)
async def cart_page(request: Request,
                    session: AsyncSession = Depends(get_session),
                    current_user: User = Depends(get_current_user_browser)
                    ):
    cart_item = await get_cart_item(session, current_user.id)
    return templates.TemplateResponse('cart.html',
                                    {'request':request,
                                     'items': cart_item})

@router.post('/delete-cart-item/')
async def delete_cart_item_front(
        item_id: int = Form(...),
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user_browser)
):
    await delete_cart_item(session, item_id, current_user.id)
    return RedirectResponse(url='/cart', status_code=303)



