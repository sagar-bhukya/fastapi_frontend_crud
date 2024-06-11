from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote

password = "Sagar@123"
encoded_password = quote(password, safe='')
DATABASE_URL = f"postgresql://postgres:{encoded_password}@localhost:5432/crud"
 
engine=create_engine(DATABASE_URL,echo=True)
Base=declarative_base()

SessionLocal=sessionmaker(bind=engine)

# def get_db():
#     db=SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()