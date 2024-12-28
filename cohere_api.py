import cohere

COHERE_API_KEY = 'hWd5UdhlLc34aba1lHLu4xYB1K8iRTxAvU0Wz3Hn'

# Initialize Cohere client
co = cohere.Client(COHERE_API_KEY)

# Function to get a standard chatbot response
def get_chat_response(user_input):
    response = co.chat(
        message=f"User: {user_input}\nChatbot:",
        temperature=0.7,
        stop_sequences=["User:"]
    )
    return response.text

# Function to get a personalized chatbot response
def get_personalized_response(user_input, mood, tone):
    prompt = (
        f"The user is feeling {mood}. Respond in a {tone} tone.\n"
        f"User: {user_input}\n"
        f"Chatbot:"
    )
    response = co.chat(
        message=prompt,
        temperature=0.7,
        stop_sequences=["User:"]
    )
    return response.text
