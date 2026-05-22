import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# TO MUSI BYĆ NA GÓRZE, PRZED UŻYCIEM DATABASE_URL
load_dotenv() 

DATABASE_URL = os.getenv("DATABASE_URL")

# Dodaj zabezpieczenie:
if DATABASE_URL is None:
    raise ValueError("Brak zmiennej DATABASE_URL w środowisku!")

engine = create_engine(DATABASE_URL)
