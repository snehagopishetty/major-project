# calm_image.py
import requests

def get_calm_image():
    api_url = "https://api.unsplash.com/photos/random"
    headers = {"Authorization": "Client-ID 2fv34XyRphU3uYtaSJiyK5kUo0C5GlZy8ty15nl-qDw"}  # Replace with your access key
    params = {"query": "calm", "orientation": "landscape"}
    response = requests.get(api_url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get("urls", {}).get("regular", "Fallback image URL")
    return "Fallback image URL"
