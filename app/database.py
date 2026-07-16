from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base 


# Establish connection to database
SQLALCHEMY_DATABASE_URL = "sqlite:///./data/database.db"


# Create the engine 
engine = create_engine(
    url=SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)


# Create a configured "Session" class
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# Create a base class for declarative models
Base = declarative_base() 


#  Create a session-factory and handler
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
