import random
from datetime import date
from faker import Faker

from models import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Load database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the SQLAlchemy engine and session factory
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
fake = Faker()


names = ["Ayman", "Ahemd", "Mohamed", "Ali", "Sayed"]
def seed_roles(db: Session):
    roles = [
        Role(name="admin", description="Full system access"),
        Role(name="hr", description="Read Policies Docs"),
        Role(name="analyst", description="Read-only analytics"),
        Role(name="viewer", description="Limited access"),
    ]
    db.add_all(roles)
    db.commit()
    return roles


def seed_departments(db: Session):

    """
    Seeds the database with predefined departments

    :param db: The database session to use
    :type db: Session
    """
    
    names = ["Engineering", "Finance", "HR", "Sales", "Operations", "Legal"]
    depts = [
        Department(name=n, description=f"{n} Department")
        for n in names
    ]
    db.add_all(depts)
    db.commit()
    return depts


def seed_employees(db: Session, departments):
    employees = []
    for _ in range(30):
        dept = random.choice(departments)
        employees.append(
            Employee(
                full_name=fake.name(),
                email=fake.unique.email(),
                job_title=fake.job(),
                employment_type=random.choice(["full-time", "contractor"]),
                salary=random.randint(30000, 120000),
                is_remote=random.choice([True, False]),
                hired_at=fake.date_between("-5y", "today"),
                department_id=dept.id,
            )
        )
    db.add_all(employees)
    db.commit()
    return employees


def seed_users(db: Session, roles):
    users = []
    for i in range(5):
        role = random.choice(roles)
        users.append(
            User(
                name = names[i],
                email=f"user{i}@enterprise.com",
                api_key=f"enterprise-key-{i}",
                role_id=role.id,
                is_active=True,
            )
        )
    db.add_all(users)
    db.commit()
    return users


def seed_revenues(db: Session, departments):
    revenues = []
    for dept in departments:
        for month in range(1, 6):
            revenues.append(
                Revenue(
                    department_id=dept.id,
                    month=date(2025, month, 1),
                    amount=random.randint(50000, 300000),
                )
            )
    db.add_all(revenues)
    db.commit()


def run_seed():
    db = SessionLocal()
    try:
        roles = seed_roles(db)
        departments = seed_departments(db)
        seed_employees(db, departments)
        seed_users(db, roles)
        seed_revenues(db, departments)
        print("✅ Enterprise database seeded successfully")
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
