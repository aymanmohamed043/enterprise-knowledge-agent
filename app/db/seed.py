from app.db.database import SessionLocal
from app.db.models import Role, User, Document, FinanceRevenue

db = SessionLocal()

# roles = [
#     Role(name="admin"),
#     Role(name="hr"),
#     Role(name="finance"),
# ]

# db.add_all(roles)
# db.commit()

# db.add(User(name="Ayman", api_key="enterprise-dev-key-123", role_id=1))

# db.add(Document(
#     title="Remote Work Policy",
#     content="Employees may work remotely up to 3 days per week...",
#     department="HR",
#     access_role="hr"
# ))

# db.add(FinanceRevenue(quarter="Q4-2024", revenue=1270000))
# db.commit()

db.add(User(name='Ahamed', api_key='hr-kwy-122', role_id=2))
db.commit()

db.close()

print("Data rows added successfully!")