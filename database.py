import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Próba pobrania zmiennej
DATABASE_URL = os.getenv("DATABASE_URL")

# 2. Diagnostyka (wyświetli co widzi aplikacja w logach podczas startu)
if DATABASE_URL:
    print(f"DEBUG: Zmienna DATABASE_URL została wczytana poprawnie.")
else:
    print("--- DIAGNOSTYKA ŚRODOWISKA ---")
    print(f"DEBUG: DATABASE_URL jest puste (None).")
    print("Dostępne zmienne środowiskowe:")
    for key in os.environ.keys():
        # Wypisujemy klucze, żeby sprawdzić czy np. nie ma literówki (np. DATABASE_URL_2)
        print(f" - {key}")
    print("------------------------------")
    raise ValueError("DATABASE_URL nie jest zdefiniowana w zmiennych środowiskowych na Railway.")

# 3. Inicjalizacja bazy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
