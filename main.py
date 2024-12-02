from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

# Configure Google Generative AI
GOOGLE_API_KEY = "AIzaSyDG1ck39g1DMxNwxydUjrHeQco96xPeZY4"  # API
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize Flask app
app = Flask(__name__)

# Initialize chat model
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

@app.route('/')
def index():
    """Serve the messaging UI."""
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    """Handle user messages and respond using Generative AI."""
    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({'error': 'Message cannot be empty.'}), 400

    # Get AI response
    try:
        response = chat.send_message(user_message, stream=False)
        ai_response = ''.join(chunk.text for chunk in response if chunk.text)
        return jsonify({'response': ai_response})
    except Exception as e:
        return jsonify({'error': f"Error generating response: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
