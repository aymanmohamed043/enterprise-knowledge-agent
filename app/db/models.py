from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.db.base import Base

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    api_key = Column(String, unique=True)
    role_id = Column(Integer, ForeignKey("roles.id"))

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    department = Column(String)
    access_role = Column(String)

class FinanceRevenue(Base):
    __tablename__ = "finance_revenue"
    id = Column(Integer, primary_key=True)
    quarter = Column(String)
    revenue = Column(Float)
