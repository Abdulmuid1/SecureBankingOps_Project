from flask import Flask, request, jsonify

# Create Flask app
app = Flask(__name__)

# Route for health check
@app.route("/health")
def health():
    return "OK", 200

# Send a payment
@app.route("/payments/send", methods=["POST"])
def send_payment():
    data = request.json
    # Respond with confirmation of payment sent
    return jsonify({"message": f"Sent ${data['amount']} to {data['to']}."})

# Get payment history
@app.route("/payments/history", methods=["GET"])
def payment_history():
    # Return a simple demo history list
    return jsonify({"history": ["payment1", "payment2", "payment3"]})

# Refund a payment
@app.route("/payments/refund", methods=["POST"])
def refund():
    data = request.json
    # Confirm the refund
    return jsonify({"message": f"Refunded ${data['amount']} to {data['to']}."})

# Run on port 5002
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
