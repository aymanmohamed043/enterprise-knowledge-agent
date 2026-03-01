from datetime import datetime, date
from sqlalchemy import (
    Column, String, Boolean, Date, DateTime,
    ForeignKey, Integer, Numeric, Text
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

# --------------------
# Roles
# --------------------
class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    users = relationship("User", back_populates="role")


# --------------------
# Users
# --------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    api_key = Column(String(255), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    role = relationship("Role", back_populates="users")

    access_logs = relationship("AccessLog", back_populates="user")


# --------------------
# Departments
# --------------------
class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255))

    employees = relationship("Employee", back_populates="department")
    revenues = relationship("Revenue", back_populates="department")


# --------------------
# Employees
# --------------------
class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    job_title = Column(String(100))
    employment_type = Column(String(50))
    salary = Column(Numeric(12, 2))
    is_remote = Column(Boolean, default=False)
    hired_at = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)

    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    department = relationship("Department", back_populates="employees")


# --------------------
# Revenues
# --------------------
class Revenue(Base):
    __tablename__ = "revenues"

    id = Column(Integer, primary_key=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    month = Column(Date, nullable=False)
    amount = Column(Integer, nullable=False)

    department = relationship("Department", back_populates="revenues")



# --------------------
# Access Logs (audit)
# --------------------
class AccessLog(Base):
    __tablename__ = "access_logs"

    id = Column(Integer, primary_key=True)
    action = Column(String(100))
    resource = Column(String(100))
    timestamp = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="access_logs")


# --------------------
# Chat History
# --------------------

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    role = Column(String) # Store the role at the time of message
    content = Column(Text) # The message text
    sender = Column(String) # "user" or "ai"
    timestamp = Column(DateTime, default=datetime.utcnow)