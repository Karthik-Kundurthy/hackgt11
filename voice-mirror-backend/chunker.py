

import argparse

print("hello")

WINDOW_SIZE=100
INCREMENT= 50

def process_document(conversation, speaker_a, speaker_b):

    conversation = conversation.replace('\n','')
    conversation = conversation.replace(speaker_a, '\n' + speaker_a)
    conversation = conversation.replace(speaker_b, '\n' + speaker_b)
    lines=conversation.split("\n")
    formatted_conv = []

    # sliding window
    N = len(lines)
    print(N)
    start = 0
    end = start + WINDOW_SIZE



    while start < N:
        print(start, end)
        if end > N:
            end = N - 1
        
        if start == end:
            break

        conv = ""
        for i in range(start,end):
            conv += lines[i]
        
        formatted_conv.append(conv)
        start += INCREMENT
        end += INCREMENT


        
    return formatted_conv
    
def process_logs(conversation):
    conversation = conversation.replace('\n','')
    conversation = conversation.replace('[', '\n[')
    lines=conversation.split("\n")
    formatted_conv = []

    # sliding window
    N = len(lines)
    print(N)
    start = 0
    end = start + WINDOW_SIZE



    while start < N:
        print(start, end)
        if end > N:
            end = N - 1
        
        if start == end:
            break

        conv = ""
        for i in range(start,end):
            conv += lines[i]
        
        formatted_conv.append(conv)
        start += INCREMENT
        end += INCREMENT


        
    return formatted_conv




def parse_conv(file_path, speaker_a, speaker_b):
    with open(file_path, 'r', encoding='utf-8') as file:
        conversation = file.read()

    conversation = conversation.replace('\n','')
    conversation = conversation.replace(speaker_a, '\n' + speaker_a)
    conversation = conversation.replace(speaker_b, '\n' + speaker_b)
    lines=conversation.split("\n")
    formatted_conv = []

    # sliding window
    N = len(lines)
    print(N)
    start = 0
    end = start + WINDOW_SIZE



    while start < N:
        print(start, end)
        if end > N:
            end = N - 1
        
        if start == end:
            break

        with open(f"sample_conv/conv_{start}_{end}.txt", "w", errors='replace') as file:
            for i in range(start,end):
                file.write(lines[i] + "\n")
        
        start += INCREMENT
        end += INCREMENT
        

            
        

    return formatted_conv

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Process two arguments -a and -b.")


    # Add arguments
    parser.add_argument('-a', type=str, help='An integer argument for -a', required=True)
    parser.add_argument('-b', type=str, help='An integer argument for -b', required=True)

    # Parse arguments
    args = parser.parse_args()
    speaker_a = args.a
    speaker_b = args.b



    conv = parse_conv(file_path="message_chunks.txt", speaker_a=speaker_a, speaker_b=speaker_b)
    print(len(conv))
    for line in conv:
        print(line)
