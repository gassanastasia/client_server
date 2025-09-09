from sqlalchemy import Column, Integer, String, DateTime, func
from datetime import datetime

from .base import Base

class Request(Base):
    __tablename__ = "requests"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(500), nullable=False)
    request_date = Column(String(10), nullable=False)
    request_time = Column(String(8), nullable=False)
    click_count = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Request(id={self.id}, text='{self.text[:20]}...')>"