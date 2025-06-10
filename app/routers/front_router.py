from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from datetime import datetime, timedelta
from app.crud import product_crud
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.order_crud import create_order_from_cart, get_order
from app.crud.product_crud import get_product_by_id
from app.db.base import get_session
from app.models.user import User
from app.routers.auth_router import get_current_user
from app.crud.cart_item_crud import create_cart_item, get_cart_item, delete_cart_item, update_cart_item
from app.routers.cart_item_router import cart_item_update
from app.routers.login_router import get_current_user_browser
from app.schemas.cart_item import CartItemCreate, CartItemUpdate

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
        variant_id: int = Form(...),
        size: float = Form(...),
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user_browser)
):
    cart_data = CartItemCreate(variant_id=variant_id, size=size, quantity=1)
    await create_cart_item(session, cart_data, current_user.id)
    return  RedirectResponse(url='/cart',status_code=303)


@router.get('/cart/', response_class=HTMLResponse)
async def cart_page(request: Request,
                    session: AsyncSession = Depends(get_session),
                    current_user: User = Depends(get_current_user_browser)
                    ):
    cart_item = await get_cart_item(session, current_user.id)
    return templates.TemplateResponse('cart.html',
                                    {'request':request,
                                     'items': cart_item})

@router.get('/product/{product_id}', response_class=HTMLResponse)
async def product_page(product_id: int,
                    request: Request,
                    session: AsyncSession = Depends(get_session),
                    ):
    product = await get_product_by_id(session, product_id)
    return templates.TemplateResponse('product.html',
                                    {'request':request,
                                     'product': product})

@router.post('/delete-cart-item/')
async def delete_cart_item_front(
        item_id: int = Form(...),
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user_browser)
):
    await delete_cart_item(session, item_id, current_user.id)
    return RedirectResponse(url='/cart', status_code=303)


@router.post('/cart/update-quantity/')
async def update_quantity_form(
        item_id: int = Form(...),
        quantity: int = Form(...),
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user_browser)
):

    cart_item_update = CartItemUpdate(quantity=quantity)

    await update_cart_item(
        session=session,
        cart_item_id=item_id,
        user_id=current_user.id,
        cart_item_update=cart_item_update
    )
    return RedirectResponse(url='/cart', status_code=303)

@router.post("/orders/create/", response_class=HTMLResponse)
async def create_order(

    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    await create_order_from_cart(session, current_user.id)
    return RedirectResponse(url="/orders", status_code=303)



@router.get("/orders/")
async def get_orders(
    request: Request,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    orders = await get_order(session, current_user.id)
    return templates.TemplateResponse("orders.html", {"request": request, "orders": orders})
