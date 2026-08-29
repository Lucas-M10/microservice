from fastapi import Header, HTTPException, status
import jwt
from config import PAYMENT_JWT_SECRET, JWT_ALGORITHM, JWT_AUDIENCE, JWT_SUBJECT

# Funcion que se encarga de verificar el token 
async def verify_token (authorization:str | None = Header (default=None, alias="Authorization")):

    if not authorization:
        raise HTTPException (
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="ERROR!! Se necesita identificacion"
        )

    authorization = authorization.strip ()


    if not authorization.startswith ("Bearer "):
        raise HTTPException (
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="ERROR!! Formato invalido"
        )

    token= authorization.replace ("Bearer ", "").strip ()

    try:

        payload = jwt.decode (
            token,
            PAYMENT_JWT_SECRET,
            algorithms= [JWT_ALGORITHM],
            audience=JWT_AUDIENCE
        )

        subject = payload.get ("sub")

        if subject != JWT_SUBJECT:
            raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail= "ERROR!! Servicio no autorizado"
            )

        return subject

    except jwt.InvalidTokenError:
        raise HTTPException (
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "ERROR!! Token invalido"
        )
