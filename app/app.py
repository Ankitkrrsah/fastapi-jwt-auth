from fastapi import FastAPI
from app.views.user_view import router as user_router

app = FastAPI()

app.include_router(user_router)