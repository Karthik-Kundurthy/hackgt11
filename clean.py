import re

# Function to clean the conversation file and retain name with message
def clean_conversation(file_path):
    # Regular expression pattern to match timestamped messages
    pattern = r'^\[\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}:\d{2}(?:\s?(AM|PM))?\] (.*?): (.*)'

    cleaned_messages = []

    # Open the conversation file
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Skip unwanted messages
            if ("This message was deleted" in line or
                "You deleted this message" in line or
                "image omitted" in line):
                continue

            # Apply the regex pattern to extract name and message
            match = re.match(pattern, line.strip())
            if match:
                sender = match.group(2)  # Extract the sender's name
                message = match.group(3)  # Extract the message
                # Append the cleaned message
                cleaned_messages.append(f"{sender}: {message}")
            else:
                # Handle multi-line messages, append to the last message
                if cleaned_messages:
                    cleaned_messages[-1] += f" {line.strip()}"

    return cleaned_messages

# Function to write the cleaned messages to a new text file
def save_cleaned_conversation(cleaned_messages, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for message in cleaned_messages:
            file.write(f"{message}\n")

# Example usage
input_file = 'whatsapp_chat.txt'  # Path to your input text file
output_file = 'cleaned_chat.txt'  # Path to save the cleaned messages

cleaned_messages = clean_conversation(input_file)
save_cleaned_conversation(cleaned_messages, output_file)