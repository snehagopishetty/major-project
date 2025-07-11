import cohere
import yake
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer


COHERE_API_KEY = 'hWd5UdhlLc34aba1lHLu4xYB1K8iRTxAvU0Wz3Hn'



# Initialize Cohere client
co = cohere.Client(COHERE_API_KEY)

# Initialize YAKE keyword extractor
kw_extractor = yake.KeywordExtractor()

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()

# Function to get a standard chatbot response
# def get_chat_response(user_input):
#     response = co.chat(
#         message=f"User: {user_input}\nChatbot:",
#         temperature=0.7,
#         stop_sequences=["User:"]
#     )
#     context_str += response.text
#     return response.text

def get_synonyms(word):
    synonyms = set()
    for syn in wn.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())  # Add the synonyms to the set
    return synonyms

# Function to get a personalized chatbot response
def get_personalized_response(user_input, mood, tone):
    # Extract keywords from user input using YAKE
    keywords = kw_extractor.extract_keywords(user_input)
    print("keywords:")
    print(keywords)

    #context handling
    filename = "context.txt"
    f = open(filename, "r")
    context_str = f.read()
    f.close()

    # Get the keyword with the highest priority (lowest score)
    if len(keywords) > 0 :
        main_keyword = min(keywords, key=lambda x: x[0])[0]  # Extract the keyword with the lowest score
    else:
        main_keyword  = ""
    # Ensure that main_keyword is a string before using split
    if isinstance(main_keyword, str):
        prompt = (
                f"You are a mental health chatbot and a mental health expert.dont mention your version or model anywhere while replying\n"
                f"The user is feeling {mood}. Respond in a {tone} tone.\n"
                f"respond while keeping in mind the previous inputs by user: {context_str}\n"
                f"respond only in english unless user asks you to respond in a certain language.\n"
                f"respond with suitable punctuations and paragraph split.\n"
                f"User: {user_input}\n"
                f"Chatbot:"
            )
        response =  co.chat(
            message=prompt,
            temperature=0.7,
            stop_sequences=["User:"]
        )

        file1 = open(filename, "a")  # append mode
        file1.write(user_input+"\n")
        file1.close()

        final_response = response.text
        # Define emotional keywords related to unwellness and emotional states
        emotional_keywords = ['stress', 'anxiety', 'depression', 'unwell', 'overwhelmed', 'sad', 'nervous', 'fear'  ]

        # Lemmatize the main keyword
        lemmatized_keyword = lemmatizer.lemmatize(main_keyword.lower())
        # Get synonyms of the lemmatized keyword
        synonyms = get_synonyms(lemmatized_keyword)

        # Check if the keyword is related to emotional states or well-being
        if lemmatized_keyword in emotional_keywords or set(synonyms).intersection(set(emotional_keywords)):
            # Generate a motivational story using the main keyword
            prompt = (
                f"The user is feeling {mood}. Respond in a {tone} tone.\n"
                f"User: {user_input}\n"
                f"Chatbot: Let me share a short story about {main_keyword} to help you feel better...\n"
                f"Story about {main_keyword}: \n"
                f"respond with suitable punctuations and paragraph split."
            )

            # Send the prompt to Cohere to generate the story
            response =  co.chat(
                message=prompt,
                temperature=0.7,
                stop_sequences=["User:"]
            )
            
            final_response = final_response + "\n\n" + response.text
            
        return final_response
