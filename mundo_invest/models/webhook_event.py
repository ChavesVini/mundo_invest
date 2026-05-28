from sqlalchemy import Column, String, DateTime
from datetime import datetime
from mundo_invest.db import Base

class WebhookEvent(Base):
    __tablename__ = "webhook_events"

    event_id = Column(String, primary_key=True, index=True)
    card_id = Column(String, nullable=False)
    processed_at = Column(DateTime, default=datetime.utcnow, nullable=False)