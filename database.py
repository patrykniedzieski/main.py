import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Upewniamy się, że pobieramy zmienną środowiskową
# Railway wstrzykuje zmienne bezpośrednio do systemu, 
# więc load_dotenv nie powinno być potrzebne, jeśli wszystko jest ustawione w panelu.
DATABASE_URL = os.getenv("DATABASE_URL")

# Dodajemy zabezpieczenie, aby od razu wiedzieć, czy zmienna istnieje
if DATABASE_URL is None:
    # Wypiszemy to w logach, abyś miał pewność, co widzi serwer
    print("BŁĄD: Zmienna środowiskowa DATABASE_URL ma wartość None!")
    raise ValueError("DATABASE_URL nie jest zdefiniowana w zmiennych środowiskowych.")

# Tworzenie silnika SQLAlchemy
engine = create_engine(DATABASE_URL)

# Tworzenie lokalnej sesji
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Klasa bazowa dla modeli
Base = declarative_base()

# Funkcja pomocnicza do pobierania sesji
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
