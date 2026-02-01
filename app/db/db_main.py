from app.db.base import Base
from app.db.database import engine
from app.db import models


if __name__ == "__main__": 
    # Create all tables in the database
    Base.metadata.create_all(bind=engine)
    print("All tables created successfully!")