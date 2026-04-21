import os
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv

load_dotenv()  # reads your .env file

API_KEY      = os.getenv("API_KEY")
API_KEY_NAME = "X-API-Key"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


def require_api_key(key: str = Security(api_key_header)):
    if key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing API key."
        )
    return key