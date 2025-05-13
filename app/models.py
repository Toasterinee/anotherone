from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from database import Base

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(40), nullable=False)
    phone = Column(String(20), nullable=False)
    message = Column(Text)
    created_at = Column(TIMESTAMP, server_default='now()')