from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.api.schemas.currency import Currency
from app.core.security import decode_jwt
from app.utils.external import request_currency_translation, get_codes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
currency_route = APIRouter(prefix="/currency", tags=["Currency"])


@currency_route.get("/list")
async def currency_list(token: str = Depends(oauth2_scheme)):
    payload = decode_jwt(token)
    if payload:
        # currency_dict = request_currency_list()
        # result_list = list(currency_dict.keys())
        return {"Currency codes": get_codes()}
    raise HTTPException(status_code=403, detail="Invalid token")


@currency_route.post("/exchange")
async def currency_translation(currency: Currency, token: str = Depends(oauth2_scheme)):
    payload = decode_jwt(token)
    if payload:
        result = request_currency_translation(currency.dict())
        return {"message": "success", "rate": result}
    raise HTTPException(status_code=403, detail="Invalid token")

