import jwt

from datetime import timedelta, datetime


ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = "JWT_SECRET_KEY"    
JWT_REFRESH_SECRET_KEY = "JWT_REFRESH_SECRET_KEY"


def create_acces_token(payload, expires_delta=None):
    if expires_delta is None:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    else:
        expires_delta = datetime.utcnow() + expires_delta

    to_encode = {"exp": expires_delta, "sun": dict(payload)}
    encode = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encode


def create_refresh_token(payload, expires_delta=None):
    if expires_delta is None:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    else:
        expires_delta = datetime.utcnow() + expires_delta

    to_encode = {"exp": expires_delta, "sun": str(payload)}
    encode = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return encode