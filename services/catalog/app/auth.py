import jwt
from typing import Literal, TypedDict

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.config import SettingsDep

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")

Role = Literal["buyer", "seller", "admin"]


class TokenUserData(TypedDict):
    sub: str
    role: Role
    id: int


def decode_token(token: str, settings, *, verify_exp: bool = True) -> dict:
    options = {"verify_exp": verify_exp}
    return jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=[settings.algorithm],
        options=options,
    )


async def get_current_user(
    settings: SettingsDep,
    token: str = Depends(oauth2_scheme),
) -> TokenUserData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token, settings)
        if payload.get("token_type") != "access":
            raise credentials_exception
        return TokenUserData(
            sub=payload["sub"],
            role=payload["role"],
            id=payload["id"],
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None
    except (jwt.PyJWTError, KeyError):
        raise credentials_exception


def required_role(role: str):
    async def dep(user: TokenUserData = Depends(get_current_user)) -> TokenUserData:
        if user["role"] != role:
            raise HTTPException(status_code=403, detail=f"Only {role}s can perform this action")
        return user
    return dep


get_current_seller = required_role("seller")
get_current_buyer = required_role("buyer")
get_current_admin = required_role("admin")