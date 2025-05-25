from fastapi import FastAPI
from app.routers import product, auth, user

app = FastAPI()

app.include_router(product.router)
app.include_router(auth.router)
app.include_router(user.router)
