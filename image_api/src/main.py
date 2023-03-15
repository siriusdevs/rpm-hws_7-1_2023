"""Main of image api."""

from fastapi import FastAPI
from .mars.router import router as mars_router
from .nasa.router import router as nasa_router
from .user.router import router as user_router

app = FastAPI(title="ImageAPI", docs_url="/")


app.include_router(user_router)
app.include_router(nasa_router)
app.include_router(mars_router)
