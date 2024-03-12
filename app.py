from flask import Flask, request, jsonify
import re

app = Flask(__name__)

email_regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

class User:
    user_id = 1
    def __init__(self, firstName, email):
        self.id = User.user_id
        self.firstName = firstName
        self.email = email
        User.user_id += 1

    def update(self, firstName=None, email=None):
        if firstName:
            self.firstName = firstName
        if email:
            self.email = email

users = {}

# Function to validate email
def is_valid_email(email):
    if re.match(email_regex, email):
        return True
    else:
        return False

# Added two initial users with ids
user1 = User("Parth", "parth.gajera@dal.ca")
user2 = User("Darshan", "darshan.patel@dal.ca")
users[str(user1.id)] = user1
users[str(user2.id)] = user2

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
    data = request.json
    if not is_valid_email(data.get('email')):
        return jsonify({"message": "Invalid email address", "success": False}), 400
    try:
        new_user = User(data['firstName'], data['email'])
        users[str(new_user.id)] = new_user
        return jsonify({"message": "User added", "success": True}), 201
    except KeyError as e:
        return jsonify({"message": "Missing data", "success": False, "error": str(e)}), 400

@app.route('/update/<id>', methods=['PUT'])
def update_user(id):
    user = users.get(id)
    if user:
        data = request.json
        if 'email' in data and not is_valid_email(data['email']):
            return jsonify({"message": "Invalid email address", "success": False}), 400
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
