import uuid
from fastapi.testclient import TestClient
from mundo_invest.main import app

client = TestClient(app)

def test_create_client_success():
    unique_email = f"claudio.{uuid.uuid4().hex[:6]}@example.com"
    
    payload = {
        "name": "Claudio Rico",
        "email": unique_email,
        "request_type": "Abertura de Conta",
        "asset_value": 250000.0
    }
    
    response = client.post("/clients", json=payload)
    
    assert response.status_code in [200, 201]
    data = response.json()
    assert data["name"] == "Claudio Rico"
    assert data["email"] == unique_email
    assert "id" in data 

def test_webhook_priority_alta():
    unique_email = f"alta.{uuid.uuid4().hex[:6]}@example.com"
    
    client.post("/clients", json={
        "name": "Claudio Alta",
        "email": unique_email,
        "request_type": "Investimento",
        "asset_value": 300000.0
    })

    webhook_payload = {
        "event_id": f"evt_{uuid.uuid4().hex[:6]}",
        "card_id": "card_alta_999",
        "email": unique_email,
        "timestamp": "2026-05-27T22:00:00Z"
    }

    response = client.post("/webhooks/pipefy/card-updated", json=webhook_payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["client_updated"]["priority"] == "prioridade_alta"
    assert data["client_updated"]["status"] == "Processado"

def test_webhook_idempotency_block():
    unique_email = f"idem.{uuid.uuid4().hex[:6]}@example.com"
    unique_event = f"evt_dup_{uuid.uuid4().hex[:6]}"

    client.post("/clients", json={
        "name": "Joao Teste",
        "email": unique_email,
        "request_type": "Suporte",
        "asset_value": 50000.0
    })

    webhook_payload = {
        "event_id": unique_event,
        "card_id": "card_joao_789",
        "email": unique_email,
        "timestamp": "2026-05-27T22:00:00Z"
    }

    first_response = client.post("/webhooks/pipefy/card-updated", json=webhook_payload)
    assert first_response.status_code == 200

    second_response = client.post("/webhooks/pipefy/card-updated", json=webhook_payload)
    assert second_response.status_code == 200
    assert second_response.json() == {"message": "Webhook already processed (idempotent)"}