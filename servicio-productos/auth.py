from fastapi import Header, status, HTTPException
import jwt
from config import PRODUCTS_JWT_SECRET, JWT_ALGORITHM, JWT_AUDIENCE, JWT_SUBJECT

# Funcion que se encarga de la autenticar una consulta 
async def verify_token (authorization: str | None = Header (default=None, alias="Authorization")):

    if not authorization:
        raise HTTPException (
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "ERROR!! Se necesita identificacion"
        )

    authorization = authorization.strip ()

    if not authorization.startswith ("Bearer "):
        raise HTTPException (
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "ERROR!! Formato de autenticacion invalido"
        )

    token= authorization.replace ("Bearer ", "")

    try:
        payload = jwt.decode (
            token,
            PRODUCTS_JWT_SECRET,
            algorithms= [JWT_ALGORITHM],
            audience= JWT_AUDIENCE
        )

        subject = payload.get ("sub")

        if subject != JWT_SUBJECT:
            raise HTTPException (
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail= "ERROR!! Servicio no autorizado"
            )

        return subject

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "ERROR!! Token invalido"
        )
