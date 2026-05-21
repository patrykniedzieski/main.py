from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import os

# Importy z Twoich plików pomocniczych
from database import get_db, Base, engine
from models import UserConfig
from security import encrypt_key, decrypt_key
from pydantic import BaseModel

# Inicjalizacja bazy danych
Base.metadata.create_all(bind=engine)

app = FastAPI()

# KONFIGURACJA (W produkcyjnym Railway używaj zmiennych środowiskowych!)
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
ALGORITHM = "HS256"

# ... [Tu wstaw swoje funkcje: verify_password, get_password_hash, authenticate_user, create_access_token, get_current_user] ...

# Schemat dla danych Empik
class EmpikRequest(BaseModel):
    api_key: str
    api_url: str

# =====================================
# ROUTES (Zintegrowane)
# =====================================

@app.post("/add-empik-config")
async def add_empik_config(
    data: EmpikRequest, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Zapisuje zaszyfrowany klucz dla zalogowanego użytkownika"""
    encrypted_key = encrypt_key(data.api_key)
    
    # Tworzymy rekord w bazie
    new_config = UserConfig(
        user_id=1, # Tutaj w przyszłości pobierz ID z current_user
        encrypted_api_key=encrypted_key, 
        api_url=data.api_url
    )
    db.add(new_config)
    db.commit()
    return {"message": "Konfiguracja Empik zapisana bezpiecznie"}

@app.get("/get-empik-config")
async def get_config(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Pobiera i odszyfrowuje klucz dla zalogowanego użytkownika"""
    config = db.query(UserConfig).filter(UserConfig.user_id == 1).first()
    if not config:
        raise HTTPException(status_code=404, detail="Brak konfiguracji")
    
    raw_key = decrypt_key(config.encrypted_api_key)
    return {"api_url": config.api_url, "api_key": "******** (odszyfrowany tylko do użycia w backendzie)"}
