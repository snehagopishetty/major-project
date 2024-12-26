from flask import Flask, render_template, request, jsonify
from cohere_api import get_chat_response
from calm_image import get_calm_image

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '')
    if not user_input:
        return jsonify({'error': 'No input provided!'}), 400

    response = get_chat_response(user_input)
    return jsonify({'response': response})

@app.route('/get_calm_image', methods=['GET'])
def get_image():
    image_url = get_calm_image()
    return jsonify({"image_url": image_url})

if __name__ == '__main__':
    app.run(debug=True)
