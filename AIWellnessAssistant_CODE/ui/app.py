from flask import Flask, request, jsonify, render_template
import uuid
import google.generativeai as genai

# 1. Setup Gemini
genai.configure(api_key="AIzaSyANqJ-Zgtjru2C3oMmpx_mQDgjSVD6Dvmk")
model = genai.GenerativeModel("gemini-1.5-flash")

# 2. Flask app
app = Flask(__name__)

def get_ai_response(user_input):
    try:
        response = model.generate_content(user_input)
        return response.text
    except Exception as e:
        return f"[Gemini Error] {str(e)}"

# 3. Serve dark-mode UI
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# 4. Handle messages from the UI
@app.route("/send", methods=["POST"])
def send():
    data = request.get_json()
    user_text = data.get("params", {}).get("text", "")
    reply = get_ai_response(user_text)
    return jsonify({
        "jsonrpc": "2.0",
        "result": reply,
        "id": data.get("id", str(uuid.uuid4()))
    })

if __name__ == "__main__":
    app.run(debug=True, port=8000)
