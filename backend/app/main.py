from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.endpoints.user import user_router
from app.api.v1.endpoints.note import note_router
from app.api.v1.endpoints.auth import auth_router
from app.api.v1.endpoints.admin import admin_router


app = FastAPI()


# CORSMiddleware required to make cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:8004"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routers
app.include_router(auth_router, prefix="/api/v1", tags=["auth"])
app.include_router(admin_router, prefix="/api/v1", tags=["admin"])
app.include_router(user_router, prefix="/api/v1", tags=["users"])
app.include_router(note_router, prefix="/api/v1", tags=["note"])
