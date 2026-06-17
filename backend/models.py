from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.sql import func
from database import Base

class URL(Base):
    __tablename__ = "urls"

    id           = Column(Integer, primary_key=True)
    short_code   = Column(String(10), unique=True, index=True, nullable=False)
    original_url = Column(Text, nullable=False)
    created_at   = Column(DateTime(timezone=True), server_default=func.now())
    click_count  = Column(Integer, default=0)

class Click(Base):
    __tablename__ = "clicks"

    id         = Column(Integer, primary_key=True)
    short_code = Column(String(10), nullable=False, index=True)
    clicked_at = Column(DateTime(timezone=True), server_default=func.now())
    user_agent = Column(Text)
    ip_address = Column(String(50))
