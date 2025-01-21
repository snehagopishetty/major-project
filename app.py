from flask import Flask, render_template, request, jsonify
from cohere_api import get_personalized_response
from calm_image import get_calm_image
from os import remove

app = Flask(__name__)

# In-memory storage for user preferences
user_preferences = {}

@app.route('/')
def index():
    filename = "context.txt"
    try:
        with open(filename, "x") as f:
            f.write("")
    except FileExistsError:
        remove(filename)
        with open(filename, "x") as f:
            f.write("")
    f.close()
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message', '')
    user_id = data.get('user_id')
    
    if not user_input:
        return jsonify({'error': 'No input provided!'}), 400

    # Retrieve user preferences
    user_profile = user_preferences.get(user_id, {"mood": "neutral", "tone": "friendly"})
    mood = user_profile["mood"]
    tone = user_profile["tone"]

    # Get personalized chatbot response
    response = get_personalized_response(user_input, mood, tone)
    return jsonify({'response': response})

@app.route('/update_preferences', methods=['POST'])
def update_preferences():
    user_id = request.json.get('user_id')
    mood = request.json.get('mood')
    tone = request.json.get('tone')

    if not user_id or not mood or not tone:
        return jsonify({'error': 'Invalid input!'}), 400

    # Save preferences in memory
    user_preferences[user_id] = {"mood": mood, "tone": tone}
    return jsonify({"message": "Preferences updated successfully!"})

@app.route('/get_calm_image', methods=['GET'])
def get_image():
    image_url = get_calm_image()
    return jsonify({"image_url": image_url})

if __name__ == '__main__':
    app.run(debug=True)
