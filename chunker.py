import numpy as np

# Function to read messages from a text file
def load_messages_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        # Strip out any unnecessary whitespace or newlines from each message
        messages = [line.strip() for line in file if line.strip()]
    return messages

# 1. Chunk messages with a sliding window (window size = 100, step size = 5)
def sliding_window_chunk(messages, window_size=10, step_size=5):
    return [messages[i:i + window_size] for i in range(0, len(messages) - window_size + 1, step_size)]

# Function to save message chunks to a text file
def save_chunks_to_file(chunks, output_filename):
    with open(output_filename, 'w', encoding='utf-8') as file:
        for chunk in chunks:
            # Join messages in each chunk with a space, and write them as a single line
            file.write(' '.join(chunk) + '\n')

# Load messages from a text file
filename = 'cleaned_chat.txt'  # Replace with your file path
messages = load_messages_from_file(filename)

# Create message groups with sliding window
message_groups = sliding_window_chunk(messages, window_size=10, step_size=5)

# Save the chunks to a new text file
output_filename = 'message_chunks.txt'  # Replace with your desired output file path
save_chunks_to_file(message_groups, output_filename)

print(f"Message chunks saved to {output_filename}")
