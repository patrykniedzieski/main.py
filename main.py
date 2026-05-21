from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import os

from database import get_db, Base, engine
from models import UserConfig
from security import encrypt_key, decrypt_key
from pydantic import BaseModel

Base.metadata.create_all(bind=engine)
app = FastAPI()

# KONFIGURACJA
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# FUNKCJE POMOCNICZE
def verify_password(plain, hashed): return pwd_context.verify(plain, hashed)
def get_password_hash(password): return pwd_context.hash(password)

# Schemat dla danych Empik
class EmpikRequest(BaseModel):
    api_key: str
    api_url: str

# TRASY
@app.post("/add-empik-config")
async def add_empik_config(data: EmpikRequest, db: Session = Depends(get_db)):
    encrypted_key = encrypt_key(data.api_key)
    new_config = UserConfig(user_id=1, encrypted_api_key=encrypted_key, api_url=data.api_url)
    db.add(new_config)
    db.commit()
    return {"message": "Konfiguracja Empik zapisana"}

@app.get("/")
def home():
    return {"status": "ok", "message": "API działa"}
