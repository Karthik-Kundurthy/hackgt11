import lanchain
from openai import OpenAI

import os

client = OpenAI(api_key=s.api_key)
completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "write a haiku about ai"}
    ], 
    
)

# langchain vectorize