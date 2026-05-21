Python
from sqlalchemy import Column, Integer, String
from database import Base

class UserConfig(Base):
    __tablename__ = "mirakl_configs"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)
    encrypted_api_key = Column(String)
    api_url = Column(String)
