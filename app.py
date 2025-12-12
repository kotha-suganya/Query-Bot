import os
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
# Configure your Gemini API key from environment variables.
# For security, do not hard-code your key.
load_dotenv()
try:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=GOOGLE_API_KEY)
except KeyError:
    print("Error: The GOOGLE_API_KEY environment variable is not set.")
    print("Please set it before running the app. On Linux/macOS: 'export GOOGLE_API_KEY=YOUR_KEY'")
    print("On Windows: 'set GOOGLE_API_KEY=YOUR_KEY'")
    exit()

# Initialize the Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the generative model and a chat history
model = genai.GenerativeModel('gemini-2.5-flash')
chat = model.start_chat(history=[])

@app.route('/')
def index():
    """Serves the main HTML page for the chatbot."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat_response():
    """Handles chat messages and returns responses from the Gemini model."""
    user_message = request.json.get("message")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # Send the user's message to the Gemini model and get a response
        response = chat.send_message(user_message).text
        return jsonify({"response": response})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the Flask development server
    app.run(debug=True)



# before running the code, just execute these 2 commands

# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
# .\venv\Scripts\activate

# as the virtual environment is created , the settings for this code are such that we need to activate it 
# each and every time . otherwise the code will not run.
# becausethe flask, google generative ai, flask core modules are installed within the virtual Environment
# for the security purpose.
# to check where the folder is restricted or not use 
# Get-ExecutionPolicy