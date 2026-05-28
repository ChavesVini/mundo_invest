from fastapi import FastAPI
from mundo_invest.db import engine, Base
from mundo_invest.routers import client_router
from mundo_invest.models.client import Client
from mundo_invest.models.webhook_event import WebhookEvent

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(client_router.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}