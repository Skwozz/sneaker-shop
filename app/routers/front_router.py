from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.crud import product_crud
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_session


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