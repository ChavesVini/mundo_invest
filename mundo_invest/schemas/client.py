from pydantic import BaseModel, EmailStr, Field

class ClientCreateSchema(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr = Field(...)
    request_type: str = Field(..., min_length=1)
    asset_value: float = Field(..., ge=0)

    class Config:
        populate_by_name = True

class ClientResponseSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
    request_type: str
    asset_value: float
    status: str
    priority: str | None = None

    class Config:
        from_attributes = True