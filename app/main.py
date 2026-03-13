from fastapi import FastAPI

from .api.v1 import router


app = FastAPI(title="Organisation API")

app.include_router(router)