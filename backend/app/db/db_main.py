from database import engine
import models


if __name__ == "__main__": 
    # Create all tables in the database
    models.Base.metadata.create_all(bind=engine)
    print("All tables created successfully!")

        