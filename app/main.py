from fastapi import FastAPI
from app.routers import product_router, auth_router,front_router ,user_router, cart_item_router, order_router
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
app = FastAPI()

app.include_router(product_router.router)
app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(cart_item_router.router)
app.include_router(order_router.router)
app.include_router(front_router.router)
app.mount('/static',StaticFiles(directory='static'), name= 'static')
templates = Jinja2Templates(directory='templates')

