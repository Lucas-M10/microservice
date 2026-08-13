from fastapi import Header, HTTPException, status

from config import VALID_TOKEN

async def verify_token (authorization:str | None = Header (default=None, alias="Authorization")):

    if not authorization:
        raise HTTPException (
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="ERROR!! Se necesita identificacion"
        )

    authorization = authorization.strip ()

    if not authorization.startswith ("Token "):
        raise HTTPException (
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="ERROR!! Formato invalido"
        )

    token = authorization.replace ("Token ", "").strip ()

    service_name = VALID_TOKEN.get (token, None)

    if not service_name:
        raise HTTPException (
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ERROR!! Token invalido"
        )

    return service_name
