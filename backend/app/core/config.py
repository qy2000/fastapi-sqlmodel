import os
import secrets

DATABASE_URL = os.environ.get("DATABASE_URL")

SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

FIRST_SUPERUSER = os.environ.get("FIRST_SUPERUSER")
FIRST_SUPERUSER_PASSWORD = os.environ.get("FIRST_SUPERUSER_PW")
