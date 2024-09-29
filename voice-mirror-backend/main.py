from dotenv import load_dotenv
import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from gemini_adapter import GeminiAdapter
from mongo_adapter import MongoAdapter, User
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt

# Load environment variables & set constants
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MONGODB_URI = os.getenv("MONGODB_URI")
JWT_SECRET_KEY = os.getenv("SECRET_KEY")
JWT_ALGORITHM = "HS256"

# Initialize clients & security
llm_client = GeminiAdapter(GEMINI_API_KEY)
db_client = MongoAdapter(MONGODB_URI)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Initialize FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper Functions
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

def create_jwt_token(username: str) -> str:
    expire = datetime.utcnow() + timedelta(days=1)
    to_encode = {"sub": username, "exp": expire}
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def verify_jwt_token(token: str) -> str:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Routes
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/signup/")
def signup_user(username: str, password: str):
    if db_client.get_user(username):
        raise HTTPException(status_code=400, detail="Username already taken")
    hashed_password = hash_password(password)
    db_client.insert_user(username, hashed_password)

@app.post("/login/")
def login_user(username: str, password: str):
    user = db_client.get_user(username)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    token = create_jwt_token(username)
    return {"access_token": token}


def authenticate_user(token: str = Depends(oauth2_scheme)) -> str:
    username = verify_jwt_token(token)
    return username

@app.post("/chat/")
def protected_route(message: str, username: str = Depends(authenticate_user)):
    response = llm_client.chat(username, message)
    return {"response": response}
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)