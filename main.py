import langchain
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
import secrets as s
from pymongo.mongo_client import MongoClient


embeddings_model = OpenAIEmbeddings(api_key=s.api_key)

import os




def get_openai_client():
    client = OpenAI(api_key=s.api_key)
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": "write a haiku about ai"}
        ], 
        
    )

    return client

embeddings = embeddings_model.embed_documents(
    [
        "Hi there!",
        "Oh, hello!",
        "What's your name?",
        "My friends call me World",
        "Hello World!"
    ]
)



uri = "mongodb+srv://karthikkundurthy:P978MHSWhtycWRC8@voicemirrorvectordb.a3on0.mongodb.net/?retryWrites=true&w=majority&appName=voiceMirrorVectorDB"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


# print(len(embeddings), len(embeddings[0]))
