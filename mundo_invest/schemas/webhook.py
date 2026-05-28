from pydantic import BaseModel, EmailStr, Field

class WebhookInputSchema(BaseModel):
    event_id: str = Field(...)
    card_id: str = Field(...)
    email: EmailStr 
    timestamp: str = Field(...)