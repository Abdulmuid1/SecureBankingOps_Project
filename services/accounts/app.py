from flask import Flask, request, jsonify

# Create Flask app
app = Flask(__name__)

# Get account info for a specific user
@app.route("/accounts/<user_id>", methods=["GET"])
def get_account(user_id):
    # Return demo account details
    return jsonify({"user_id": user_id, "account": "Demo account details"})

# Update account info
@app.route("/accounts/update", methods=["POST"])
def update_account():
    data = request.json
    # Respond with confirmation and the new data
    return jsonify({"message": "Account updated", "new_data": data})

# Delete an account
@app.route("/accounts/delete", methods=["DELETE"])
def delete_account():
    data = request.json
    # Confirm deletion
    return jsonify({"message": f"Account {data['user_id']} deleted"})

# Run on port 5001
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
