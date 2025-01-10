from flask import Flask, render_template, request, jsonify
from faq import match_intent, faq_data  # Importing logic from faq.py

app = Flask(__name__)

# Serve the HTML page (index.html) on the home route
@app.route('/')
def home():
    return render_template('index.html')

# Chatbot route to handle the POST requests from the frontend
@app.route("/chatbot", methods=["POST"])
def chatbot():
    user_query = request.json.get("query")
    if not user_query:
        return jsonify({"response": "Invalid query. Please provide a valid input."})

    # Call match_intent function from faq.py
    intent = match_intent(user_query)

    # Generate response using faq_data from faq.py
    response = faq_data.get(intent, "I'm sorry, I couldn't understand that. Can you rephrase?")
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
