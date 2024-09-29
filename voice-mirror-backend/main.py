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
from pydantic import BaseModel
import jwt
from pymongo.mongo_client import MongoClient
from langchain_community.llms import OpenAI
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from pymongo.operations import SearchIndexModel


# Load environment variables & set constants
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MONGODB_URI = os.getenv("MONGODB_URI")
JWT_SECRET_KEY = os.getenv("SECRET_KEY")
JWT_ALGORITHM = "HS256"
CLUSTER_NAME = "voiceMirrorVectorDB"
DB_NAME = "voicemirror"
EMBEDDING_SIZE = 1536
CONVERSATION_COLLECTION = "conversations"


# Initialize clients & security
llm_client = GeminiAdapter(GEMINI_API_KEY)
db_client = MongoAdapter(MONGODB_URI)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
embeddings_model = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
client = MongoClient(MONGODB_URI)
database = client[DB_NAME]
collection = database[CONVERSATION_COLLECTION]

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
def ping_uri():
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

ping_uri() 

def hash_password(password: str) -> str:
    return password
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return password == hashed_password
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
    
def authenticate_user(token: str = Depends(oauth2_scheme)) -> str:
    username = verify_jwt_token(token)
    return username

# ref: https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-stage/
def get_search_pipeline(persona, query_text):
    # define pipeline
    # vector matching and filters by user and personality
    query_vector = embeddings_model.embed_documents([query_text])[0]
    pipeline = [
        {
            '$vectorSearch': {
                'index': "default",
                'path': 'text_embedding',
                'queryVector': query_vector,
                'numCandidates': 30,
                'limit': 10
            }
        },
        {
            '$match': {
                # 'username': recipient,
                'persona': persona
            }
        },
        {
            '$project': {
                'raw_text': 1,  
                'conversation_id': 1,
                'score': {
                    '$meta': 'vectorSearchScore'
                }
            }
        }
    ]
    
    return pipeline


# Routes
@app.get("/")
def read_root():
    return {"Hello": "World"}

class SignupRequest(BaseModel):
    username: str
    password: str

@app.post("/signup/")
def signup_user(signup_request: SignupRequest):
    if db_client.get_user(signup_request.username):
        raise HTTPException(status_code=400, detail="Username already taken")
    hashed_password = hash_password(signup_request.password)
    db_client.insert_user(signup_request.username, hashed_password)

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login/")
def login_user(login_request: LoginRequest):
    user = db_client.get_user(login_request.username)
    if not user or not verify_password(login_request.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    token = create_jwt_token(login_request.username)
    return {"access_token": token}

class ChatRequest(BaseModel):
    message: str

@app.post("/chat/")
def protected_route(chat_request: ChatRequest, username: str = Depends(authenticate_user)):
    response = llm_client.chat(username, chat_request.message)
    return {"reply": response}

def addData(persona, recipient, text_chunk):
    
    # create text embedding
    try:
        embedding_vector = embeddings_model.embed_documents([text_chunk])[0]
    except Exception as e:
        embedding_vector= None
        return {"message": "could not embed"}

    # create document and insert
    now = datetime.datetime.now()
    document = {
        "username": recipient,
        "persona": persona,
        "raw_text": text_chunk,
        "conversation_id": f"{recipient}:{persona}:{now}",
        "text_embedding": embedding_vector  # Adding generated embedding vector
    }

    try:
        result = collection.insert_one(document) 
        return {"message": "Data inserted successfully", "document_id": str(result.inserted_id)}
    except Exception as e:
        return {"error": f"Failed to insert data into MongoDB: {str(e)}"} 


@app.post("/add_data")
def parse_and_add_data(persona, recipient, file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        chunks = file.read().split("\n")
    
    for index, chunk in enumerate(chunks):
        if chunk.strip():
            response = addData(
                recipient=recipient,
                persona=persona,
                text_chunk=chunk
            )

        print(f"Inserted chunk {index + 1}: {response}")

    pass

@app.post("/search")
def run_vector_search(persona, query_text):
    pipeline = get_search_pipeline(persona, query_text)
    results = collection.aggregate(pipeline)
    return results

@app.post("/example_search")
def sample_conversation_search():
    file_path = "message_chunks.txt"
    with open(file_path, 'r', encoding='utf-8') as file:
        chunks = file.read().split("\n")
    
    test = chunks[0]
    results = run_vector_search("karthik", "harish", test)
    for result in list(results):
        print(result['raw_text'], '\n')

    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)