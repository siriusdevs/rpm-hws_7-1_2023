from fastapi import HTTPException, status
from config import TOKEN


def check_auth(auth: str):
    if auth != TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="WRONG AUTH TOKEN",
        )
