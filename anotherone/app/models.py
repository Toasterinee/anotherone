# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Boolean
from sqlalchemy.sql import func
from app.database import Base

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(length=40), nullable=False)
    phone = Column(String(length=20), nullable=False)
    message = Column(String(length=255), nullable=False)
    agreement = Column(Boolean, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    def __init__(self, full_name, phone, message, agreement):
        self.full_name = full_name
        self.phone = phone
        self.message = message
        self.agreement = agreement