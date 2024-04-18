from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.services.utils import get_logger
from routers import users, coins

logger = get_logger(__name__)

app = FastAPI(title="Crypto API")

app.include_router(users.router)
app.include_router(coins.router)


@app.get("/", response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url="/docs")
