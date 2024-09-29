import langchain
from langchain_community.llms import OpenAI
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
import secrets as s
from pymongo.mongo_client import MongoClient
from requests.auth import HTTPDigestAuth
# from langchain_mongodb.vectorstores import MongoDBAtlasVectorSearch
from langchain_community.document_loaders import DirectoryLoader
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
# import key_param
import json
import os
import requests
import getpass
from pymongo.operations import SearchIndexModel
import datetime
import asyncio


embeddings_model = OpenAIEmbeddings(api_key=s.api_key)



# Create a new client and connect to the server
uri = s.uri
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Key constants
PUBLIC_KEY = s.public_key
PRIVATE_KEY = s.private_key
GROUP_ID = "66f75b9164ca15604af8510b"
CLUSTER_NAME = "voiceMirrorVectorDB"
DB_NAME = "voicemirror"
EMBEDDING_SIZE = 1536
INDEX_CREATION_URL =f"https://cloud.mongodb.com/api/atlas/v1.0/groups/{GROUP_ID}/clusters/{CLUSTER_NAME}/fts/indexes"
CONVERSATION_COLLECTION = "conversations"

# pulled from documentation
database = client[DB_NAME]
collection = database[CONVERSATION_COLLECTION]


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
# ref: https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-stage/
def get_search_pipeline(persona, recipient, query_text):
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

def run_vector_search(persona, recipient, query_text):
    pipeline = get_search_pipeline(recipient, persona, query_text)
    results = collection.aggregate(pipeline)
    return results

def sample_conversation_search():
    file_path = "message_chunks.txt"
    with open(file_path, 'r', encoding='utf-8') as file:
        chunks = file.read().split("\n")
    
    test = chunks[0]
    results = run_vector_search("karthik", "harish", test)
    for result in list(results):
        print(result['raw_text'], '\n')

# Prefilling database
if __name__ == "__main__":

    sample_conversation_search()




