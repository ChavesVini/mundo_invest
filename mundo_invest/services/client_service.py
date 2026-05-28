from sqlalchemy.orm import Session
from mundo_invest.models.client import Client
from mundo_invest.models.webhook_event import WebhookEvent
from mundo_invest.clients.pipefy_client import PipefyClient
from fastapi import HTTPException, status

from mundo_invest.schemas.webhook import WebhookInputSchema

class ClientService:
    def __init__(self, db: Session):
        self.db = db
        self.pipefy_client = PipefyClient()

    def create_client(self, schema_input):
        new_client = Client(
            name=schema_input.name,
            email=schema_input.email,
            request_type=schema_input.request_type,
            asset_value=schema_input.asset_value,
            status="Aguardando Análise"
        )
        
        self.db.add(new_client)
        self.db.commit()
        self.db.refresh(new_client)

        self.pipefy_client.create_card(
            name=new_client.name,
            email=new_client.email,
            request_type=new_client.request_type,
            asset_value=new_client.asset_value
        )
        
        return new_client

    def process_webhook(self, webhook_data: WebhookInputSchema):
        already_processed = self.db.query(WebhookEvent).filter(WebhookEvent.event_id == webhook_data.event_id).first()
        if already_processed:
            return {"message": "Webhook already processed (idempotent)"}

        client = self.db.query(Client).filter(Client.email == webhook_data.email).first()
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente com o e-mail {webhook_data.email} não encontrado."
            )

        if client.asset_value >= 200000:
            client.priority = "prioridade_alta"
        else:
            client.priority = "prioridade_normal"

        client.status = "Processado"

        try:
            self.pipefy_client.update_card_fields(
                card_id=webhook_data.card_id,
                status=client.status,
                priority=client.priority
            )
        except Exception as e:
            print(f"Aviso: Falha ao enviar dados ao Pipefy via GraphQL: {e}")

        new_event = WebhookEvent(
            event_id=webhook_data.event_id,
            card_id=webhook_data.card_id
        )
        self.db.add(new_event)
        self.db.commit()
        self.db.refresh(client)

        return {
            "message": "Webhook processado com sucesso e integrado ao Pipefy via GraphQL",
            "client_updated": {
                "id": client.id,
                "name": client.name,
                "email": client.email,
                "status": client.status,
                "priority": client.priority
            }
        }