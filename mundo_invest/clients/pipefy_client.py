import logging

logger = logging.getLogger(__name__)

class PipefyClient:
    def __init__(self):
        self.url = "https://api.pipefy.com/graphql" 
        self.pipe_id = 301234567

    def create_card(self, name: str, email: str, request_type: str, asset_value: float) -> dict:
        mutation = """
        mutation CreateNewCard($input: CreateCardInput!) {
          createCard(input: $input) {
            clientMutationId
            card {
              id
              title
              url
            }
          }
        }
        """
        
        variables = {
            "input": {
                "pipe_id": 301234567,
                "title": f"Solicitação - {name}",
                "fields_attributes": [
                    {"field_id": "email", "field_value": email},
                    {"field_id": "request_type", "field_value": request_type},
                    {"field_id": "asset_value", "field_value": str(asset_value)}
                ]
            }
        }
        
        print(f"\nSimulando Pipefy GraphQL - Mutation:\n{mutation}")
        print(f"Simulando Pipefy GraphQL - Variables: {variables}")
        
        return {
            "clientMutationId": "sync_abc123",
            "card": {
                "id": "card_gerado_999",
                "title": f"Solicitação - {name}",
                "url": "https://app.pipefy.com/open-cards/999"
            }
        }

    def update_card_fields(self, card_id: str, status: str, priority: str) -> dict:
        mutation = """
        mutation UpdateCardFields($inputStatus: UpdateCardFieldInput!, $inputPriority: UpdateCardFieldInput!) {
          updateStatus: updateCardField(input: $inputStatus) {
            success
            clientMutationId
          }
          updatePriority: updateCardField(input: $inputPriority) {
            success
            clientMutationId
          }
        }
        """
        
        variables = {
            "inputStatus": {
                "card_id": card_id,
                "field_id": "status",
                "new_value": [status]
            },
            "inputPriority": {
                "card_id": card_id,
                "field_id": "priority",
                "new_value": [priority]
            }
        }

        print(f"Simulando Pipefy GraphQL Update - Mutation: {mutation}")
        print(f"Simulando Pipefy GraphQL Update - Variables: {variables}")

        return {
            "data": {
                "updateStatus": {
                    "success": True,
                    "clientMutationId": "sync_status_123",
                    "card": {
                        "id": card_id
                    }
                },
                "updatePriority": {
                    "success": True,
                    "clientMutationId": "sync_priority_123",
                    "card": {
                        "id": card_id
                    }
                }
            }
        }