Tutorial 5: Back-End Frameworks 1 

* *Date Created*: 10 Mar 2024
* *Last Modification Date*: 11 Mar 2024
* *Lab URL*: <https://dal.brightspace.com/d2l/le/content/311813/viewContent/4041531/View>
* *Tutorial 5 Link (Gitlab):* <https://git.cs.dal.ca/pgajera/csci-5709-tutorials/-/tree/main/Tutorial5>
* *Deployed App Link (Render):* <https://tutorial-5-a7as.onrender.com/users>

**Note:** As I have used "Render" for the deployement of my app and I am using its free version it might take some time to show the reponse for the first time.

## Author

* [Parth Chhaganlal Gajera](pr769932@dal.ca)

## Built With

* [Flask](https://flask.palletsprojects.com/) - The web framework used to build the application.
* [Visual Studio Code](https://code.visualstudio.com/) - Used for writing and debugging code.
* [Render](https://render.com/) - Used for hosting the website.

## Sources Used

### app.py

*Lines 1-67*

```
from flask import Flask, request, jsonify

app = Flask(__name__)

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

listOfUsers = []

users = {}

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
    try:
        data = request.json
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

```
Here the above code written in flask for  creating a simple REST API using python. The reference is taken from the websites mentioned below:

1. The Route made for different endpoints is taken from the [Routing in flask website of "HackersandSlackers".](https://hackersandslackers.com/flask-routes/)

2. For sending the JSON repsonse in flask is taken from the website [How to return a JSON response from a Flask API of "Geeks for Geeks"](https://www.geeksforgeeks.org/how-to-return-a-json-response-from-a-flask-api/)

## Acknowledgments

I have learn how to use the route for making endpoints  and also how to handle data in backend from the [official documentation of Flask](https://flask.palletsprojects.com/).