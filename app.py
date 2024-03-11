from flask import Flask, request, jsonify
import json
import uuid

app = Flask(__name__)

class User:
    def __init__(self, id, firstName, email):
        self.id = id
        self.firstName = firstName
        self.email = email

    def update(self, firstName=None, email=None):
        if firstName:
            self.firstName = firstName
        if email:
            self.email = email

listOfUsers = []

# Utilize a dictionary for quicker access via user ID
users = {}

# Add two initial users with ids
user1 = User(str(uuid.uuid4()), "ABC", "abc@abc.ca")
user2 = User(str(uuid.uuid4()), "XYZ", "xyz@xyz.ca")
users[user1.id] = user1
users[user2.id] = user2

@app.route('/users', methods=['GET'])
def get_all_users():
    user_list = [vars(user) for user in users.values()]
    return jsonify({
        "message": "Users retrieved",
        "success": True,
        "users": user_list
    })

@app.route('/add', methods=['POST'])
def add_user():
    try:
        data = request.json
        new_user = User(str(uuid.uuid4()), data['firstName'], data['email'])
        users[new_user.id] = new_user
        return jsonify({"message": "User added", "success": True}), 201
    except KeyError as e:
        return jsonify({"message": "Missing data", "success": False, "error": str(e)}), 400

@app.route('/update/<id>', methods=['PUT'])
def update_user(id):
    user = users.get(id)
    if user:
        data = request.json
        user.update(firstName=data.get('firstName'), email=data.get('email'))
        return jsonify({"message": "User updated", "success": True})
    else:
        return jsonify({"message": "User not found", "success": False}), 404

@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    user = users.get(id)
    if user:
        return jsonify({"success": True, "user": vars(user)})
    else:
        return jsonify({"message": "User not found", "success": False}), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
