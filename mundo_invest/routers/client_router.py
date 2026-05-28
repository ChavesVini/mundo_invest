from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from mundo_invest.db import get_db
from mundo_invest.schemas.client import ClientCreateSchema, ClientResponseSchema
from mundo_invest.schemas.webhook import WebhookInputSchema
from mundo_invest.services.client_service import ClientService

router = APIRouter()

@router.post("/clients", response_model=ClientResponseSchema)
def create_client(schema_input: ClientCreateSchema, db: Session = Depends(get_db)):
    service = ClientService(db) 
    return service.create_client(schema_input)

@router.post("/webhooks/pipefy/card-updated")
def process_webhook(webhook_input: WebhookInputSchema, db: Session = Depends(get_db)):
    service = ClientService(db)
    return service.process_webhook(webhook_input)