"""Main of image api."""

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .mars.router import router as mars_router
from .nasa.router import router as nasa_router
from .user.router import router as user_router

app = FastAPI(title="ImageAPI", docs_url="/")

origins = [
    "http://localhost:8001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

app.include_router(user_router)
app.include_router(nasa_router)
app.include_router(mars_router)
