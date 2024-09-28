# from sentence_transformers import SentenceTransformer
import numpy as np
# import faiss

# # Initialize the model
# model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to read messages from a text file
def load_messages_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        # Strip out any unnecessary whitespace or newlines from each message
        messages = [line.strip() for line in file if line.strip()]
    return messages

# 1. Chunk messages with a sliding window (window size = 10, step size = 5)
def sliding_window_chunk(messages, window_size=10, step_size=5):
    return [messages[i:i + window_size] for i in range(0, len(messages) - window_size + 1, step_size)]

# Load messages from a text file
filename = 'cleaned_chat.txt'  # Replace with your file path
messages = load_messages_from_file(filename)

# Create message groups with sliding window
message_groups = sliding_window_chunk(messages, window_size=10, step_size=5)

# Print out the first few message groups as an example
for group in message_groups[:3]:
    print(group)
