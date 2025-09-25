# Import Flask to create a web application and handle HTTP requests
from flask import Flask, request, jsonify

# Create the Flask app
app = Flask(__name__)

# Route for health check
@app.route("/health")
def health():
    return "OK", 200
    
# Route for user signup
@app.route("/signup", methods=["POST"])
def signup():
    # Get JSON data sent by the client
    data = request.json
    # Return a message confirming user creation
    return jsonify({"message": f"User {data['username']} created!"})

# Route for user login
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    # Respond with a welcome message and a fake JWT token
    return jsonify({"message": f"Welcome back {data['username']}", "token": "fake-jwt-token"})

# Route to refresh JWT token
@app.route("/refresh-token", methods=["POST"])
def refresh():
    # Return a new fake token
    return jsonify({"token": "new-fake-jwt-token"})

# Run the app on all network interfaces, port 5000
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
