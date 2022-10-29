from sqlalchemy.orm import declarative_base
from sqlalchemy import DateTime, Column, Integer, String
from datetime import datetime

Base = declarative_base()


class Algorithms(Base):
    """Database model for parsed data."""
    __tablename__ = 'Algorithms'

    id = Column(Integer, primary_key=True)
    operation = Column(String)
    complexity = Column(String)
    example = Column(String)
    type = Column(Integer)


class Users(Base):
    """Database model for authorized users."""
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_request = Column(DateTime)




