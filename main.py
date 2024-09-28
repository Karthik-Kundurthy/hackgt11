import langchain
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
import secrets as s

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
# print(len(embeddings), len(embeddings[0]))
