from fastapi import FastAPI
from app.routers import product_router, auth_router, user_router, cart_item_router, order_router

app = FastAPI()

app.include_router(product_router.router)
app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(cart_item_router.router)
app.include_router(order_router.router)
