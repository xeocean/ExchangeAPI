import asyncio
import uvicorn

from fastapi import FastAPI
from starlette.responses import RedirectResponse
from app.api.endpoints.users import router_user
from app.api.endpoints.currency import currency_route
from app.db.database import init_db

app = FastAPI()
app.include_router(router_user)
app.include_router(currency_route)


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    asyncio.run(init_db())
    uvicorn.run(app, host="127.0.0.1", port=8000)

