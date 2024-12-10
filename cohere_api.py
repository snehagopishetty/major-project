import cohere

COHERE_API_KEY = 'hWd5UdhlLc34aba1lHLu4xYB1K8iRTxAvU0Wz3Hn'

def get_chat_response(user_input):
    co = cohere.Client(COHERE_API_KEY)
    response = co.chat(
       # model='command-xlarge-2023',
        message=f"User: {user_input}\nChatbot:",
        #max_tokens=50,
        temperature=0.7,
        stop_sequences=["User:"])
    #return response.generations[0].text.strip()
    return response.text
    
