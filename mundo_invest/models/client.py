from sqlalchemy import Column, Integer, String, Float
from mundo_invest.db import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    request_type = Column(String, nullable=False)
    asset_value = Column(Float, nullable=False)
    status = Column(String, default="Aguardando Análise", nullable=False)
    priority = Column(String, nullable=True)