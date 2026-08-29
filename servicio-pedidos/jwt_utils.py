import jwt

from config import JWT_ALGORITHM, JWT_SUBJECT

def generate_jwt (secret:str, audience:str)->str:

    payload = {
        "sub": JWT_SUBJECT,
        "aud": audience,
    }

    token = jwt.encode (
        payload=payload,
        key=secret,
        algorithm= JWT_ALGORITHM
    )

    return token