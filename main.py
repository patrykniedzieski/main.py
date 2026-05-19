from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

# =====================================
# APP CONFIG
# =====================================

app = FastAPI()

SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# =====================================
# PASSWORD CONFIG
# =====================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)

# =====================================
# USERS DATABASE
# =====================================

# login:
# username = admin
# password = admin123

fake_users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": pwd_context.hash("admin123")
    }
}

# =====================================
# PASSWORD FUNCTIONS
# =====================================

def verify_password(
    plain_password: str,
    hashed_password: str
):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )

def get_password_hash(password: str):
    return pwd_context.hash(password)

# =====================================
# AUTH FUNCTIONS
# =====================================

def authenticate_user(
    username: str,
    password: str
):

    user = fake_users_db.get(username)

    if not user:
        return False

    if not verify_password(
        password,
        user["hashed_password"]
    ):
        return False

    return user

def create_access_token(
    data: dict,
    expires_delta: timedelta = None
):

    to_encode = data.copy()

    expire = datetime.utcnow() + (
        expires_delta
        or timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    to_encode.update({
        "exp": expire
    })

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt

async def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials"
    )

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = fake_users_db.get(username)

    if user is None:
        raise credentials_exception

    return user

# =====================================
# ROUTES
# =====================================

@app.get("/")
def home():
    return {
        "status": "ok",
        "message": "API działa poprawnie 🚀"
    }

@app.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):

    user = authenticate_user(
        form_data.username,
        form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_access_token(
        data={
            "sub": user["username"]
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.get("/protected")
async def protected_route(
    current_user: dict = Depends(
        get_current_user
    )
):

    return {
        "message": f"Witaj {current_user['username']}"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
