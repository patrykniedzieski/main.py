from cryptography.fernet import Fernet
import os

# Klucz musisz dodać w Railway w sekcji Variables jako ENCRYPTION_KEY
key = os.getenv("ENCRYPTION_KEY").encode() 
cipher = Fernet(key)

def encrypt_key(plain_key: str) -> str:
    return cipher.encrypt(plain_key.encode()).decode()

def decrypt_key(encrypted_key: str) -> str:
    return cipher.decrypt(encrypted_key.encode()).decode()
