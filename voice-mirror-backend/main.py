from dotenv import load_dotenv
import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from gemini_adapter import GeminiAdapter
from mongo_adapter import MongoAdapter
import bcrypt
from datetime import datetime, timedelta
from pydantic import BaseModel
import jwt
from pymongo.mongo_client import MongoClient
from langchain_community.llms import OpenAI
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from pymongo.operations import SearchIndexModel
from chunker import process_document, process_logs


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
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

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
def get_search_pipeline(username, persona, query_text):
    query_vector = embeddings_model.embed_documents([query_text])[0]
    pipeline = [
        {
            '$vectorSearch': {
                'index': "default",
                'path': 'text_embedding',
                'queryVector': query_vector,
                'filter': {
                    'username': username,
                    'persona': persona
                },
                'numCandidates': 30,
                'limit': 1
            }
        },
        {
            '$project': {
                'raw_text': 1,
            }
        }
    ]

    return pipeline

def addData(username, persona, text_chunk):
    try:
        embedding_vector = embeddings_model.embed_documents([text_chunk])[0]
    except Exception as e:
        embedding_vector= None
        return {"message": "could not embed"}

    now = datetime.now()
    document = {
        "username": username,
        "persona": persona,
        "raw_text": text_chunk,
        "conversation_id": f"{username}:{persona}:{now}",
        "text_embedding": embedding_vector  # Adding generated embedding vector
    }

    try:
        result = collection.insert_one(document)
        return {"message": "Data inserted successfully", "document_id": str(result.inserted_id)}
    except Exception as e:
        return {"error": f"Failed to insert data into MongoDB: {str(e)}"}

# Routes
@app.get("/")
def read_root():
    return {"Hello": "World"}

class SignupRequest(BaseModel):
    username: str
    password: str

@app.post("/signup")
def signup_user(signup_request: SignupRequest):
    if db_client.get_user(signup_request.username):
        raise HTTPException(status_code=400, detail="Username already taken")
    hashed_password = hash_password(signup_request.password)
    db_client.insert_user(signup_request.username, hashed_password)

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
def login_user(login_request: LoginRequest):
    user = db_client.get_user(login_request.username)
    if not user or not verify_password(login_request.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    token = create_jwt_token(login_request.username)
    return {"access_token": token}

class ChatRequest(BaseModel):
    persona: str
    message: str
    threadId: str   

@app.post("/chat")
def protected_route(chat_request: ChatRequest, username: str = Depends(authenticate_user)):
    pipeline = get_search_pipeline(username, chat_request.persona, chat_request.message)
    results = list(collection.aggregate(pipeline))
    context = None
    if results:
        context = results[0]["raw_text"]
    
    response = llm_client.chat(username, chat_request.persona, chat_request.message, chat_request.threadId, context)
    return {"reply": response}

class ModifyPersonaRequest(BaseModel):
    username: str
    persona: str
    description: str
    documents: list

@app.post("/add_persona")
def add_persona(persona_request: ModifyPersonaRequest):
    print(persona_request)
    if not db_client.get_user(persona_request.username):
        raise HTTPException(status_code=400, detail="Username doesn't exist")
    
    db_client.add_persona(
        persona_request.username, 
        persona_request.persona, 
        persona_request.description, 
    )

    for document in persona_request.documents:
        chunks = process_logs(document)
        for chunk in chunks:
            addData(persona_request.username, persona_request.persona, chunk)

@app.post("/edit_persona")
def edit_persona(persona_request: ModifyPersonaRequest):
    user = db_client.get_user(persona_request.username)
    if not user or not any(persona.persona == persona_request.persona for persona in user.personas):
        raise HTTPException(status_code=400, detail="Username doesn't exist")
    
    db_client.edit_persona(
        persona_request.username,
        persona_request.persona,
        persona_request.description
    )

    for document in persona_request.documents:
        chunks = process_logs(document)
        for chunk in chunks:
            addData(persona_request.username, persona_request.persona, chunk)

class PersonaRequest(BaseModel):
    username: str

@app.post("/get_personas")
def get_personas(persona_request: PersonaRequest):
    user = db_client.get_user(persona_request.username)
    if not user:
        raise HTTPException(status_code=400, detail="Username doesn't exist")

    return {"personas": user.personas}


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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
