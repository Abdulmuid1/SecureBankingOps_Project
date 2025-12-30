# Import Flask to create a web application and handle HTTP requests
from flask import Flask, request, jsonify

# Import Prometheus tools
# generate_latest: Grabs all the data from the counters
# CONTENT_TYPE_LATEST: Tells the browser it's Prometheus data
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

"""
    Define Custom Metrics
    - Counter for failed logins
    - Counter for successful logins
"""
LOGIN_FAILURES = Counter('auth_login_failures_total', 'Total failed login attempts')
LOGIN_SUCCESS = Counter('auth_login_success_total', 'Total successful logins')

# Create the Flask app
app = Flask(__name__)

# Route for Metrics
@app.route('/metrics')
def metrics():
    # Return the current value of all counters
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

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
    username = data.get('username', 'unknown')
    password = data.get('password', '')

    # Check password
    # If password is wrong, increment failed logins!
    if password == "wrong":
        LOGIN_FAILURES.inc()  # increment failed logins
        return jsonify({"error": "Invalid credentials"}), 401

    # If password is right, increment successful logins!
    LOGIN_SUCCESS.inc()   # increment successful logins

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