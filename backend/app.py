from flask import (
    Flask,
    redirect,
    url_for,
    session,
    send_from_directory,
    render_template,
    jsonify,
    request,
)
from authlib.integrations.flask_client import OAuth
from authlib.common.security import generate_token
import os
from pymongo import MongoClient
from bson.objectid import ObjectId

# region Debug Output

# for ease of debugging, debug output will be written to debug_out.txt
DEBUG_FILE = "debug_out.txt"

# clear debug file in startup
if DEBUG_FILE:
    with open(DEBUG_FILE, "w") as f:
        f.write("DEBUG LOG\n")


# function to write to debug file
def debug_out(message: str):
    if DEBUG_FILE:
        with open(DEBUG_FILE, "a") as f:
            f.write(str(message) + "\n")


# endregion Debug Output

static_path = os.getenv("STATIC_PATH", "static")
template_path = os.getenv("TEMPLATE_PATH", "templates")
isDevEnv = os.getenv("FLASK_ENV", "production") == "development"


app = Flask(__name__, static_folder=static_path, template_folder=template_path)
app.secret_key = os.urandom(24)


oauth = OAuth(app)

nonce = generate_token()


oauth.register(
    name=os.getenv("OIDC_CLIENT_NAME"),
    client_id=os.getenv("OIDC_CLIENT_ID"),
    client_secret=os.getenv("OIDC_CLIENT_SECRET"),
    # server_metadata_url='http://dex:5556/.well-known/openid-configuration',
    authorization_endpoint="http://localhost:5556/auth",
    token_endpoint="http://dex:5556/token",
    jwks_uri="http://dex:5556/keys",
    userinfo_endpoint="http://dex:5556/userinfo",
    device_authorization_endpoint="http://dex:5556/device/code",
    client_kwargs={"scope": "openid email profile"},
)


# Wrapper object for interacting with database
class MongoWrapper:
    def __init__(self, uri):
        self.client = MongoClient(uri)

    def getDatabase(self, dbName):
        db = self.client[dbName]
        return db

    def getCollection(self, dbName, colName):
        col = self.getDatabase(dbName)[colName]
        return col

    # Insert a single document into the specified collection in the specified collection
    # The dict that is passed in will have an ObjectID added to it
    def insertDocument(self, dbName, colName, jsonObj):
        return self.getCollection(dbName, colName).insert_one(jsonObj)

    # Find a singe document in the specified collection in the specified collection
    # Returns with a the first matching document
    # A document is a match if all keys:value pairs in the query dict are present and match
    def findDocument(self, dbName, colName, jsonObj={}):
        return self.getCollection(dbName, colName).find_one(jsonObj)

    # Find all documents in the specified collection in the specified collection
    # Returns with an iterable containing matching documents
    # A document is a match if all keys:value pairs in the query dict are present and match
    def searchDocument(self, dbName, colName, jsonObj={}):
        return self.getCollection(dbName, colName).find(jsonObj)

    # Update a singe document in the specified collection in the specified collection
    # Updates with a the first matching document
    # A document is a match if all keys:value pairs in the query dict are present and match
    # All key:value pairs in the values dict will be added or override those in the document
    def updateDocument(self, dbName, colName, valuesToSet, jsonObj={}):
        update_operation = {"$set": valuesToSet}
        return self.getCollection(dbName, colName).update_one(jsonObj, update_operation)


# create a wrapper object using the URI
mongo = MongoWrapper(os.getenv("MONGO_URI"))
# print(os.getenv("MONGO_URI"))

DB_USERS = "usersdb"
COL_USERS = "users"

"""Function to add Dex accounts to Database
This is hardcoded, it is not synced with Dex.
"""
def addDexUsers():
    users = [
        {
            "email": "admin@hw3.com",
            "hash": "$2b$10$8NoCpIs/Z6v0s/pU9YxYIO10uWyhIVOS2kmNac9AD0HsqRhP5dUie",  # password = "password"
            "username": "admin",
            "userID": "123",
        },
        {
            "email": "moderator@hw3.com",
            "hash": "$2b$12$2aaoZyVjMWvoCq.DmCUECOGoW0oaBCyzSluUm3BpLrP26sVT71PSC",  # password = "mpassword"
            "username": "moderator",
            "userID": "456",
        },
        {
            "email": "user@hw3.com",
            "hash": "$2b$12$321HomfT164U9f5l.xQaYuHThGCss8PRPNy8t./tq8Frgr6UYeEka",  # password = "upassword"
            "username": "user",
            "userID": "789",
        },
    ]
    for user in users:
        find = mongo.findDocument(
            DB_USERS,
            COL_USERS,
            {
                "email": user["email"],
                # "userID": user["userID"],
            },
        )
        if not find:
            mongo.insertDocument(
                DB_USERS,
                COL_USERS,
                {
                    "email": user["email"],
                    "username": user["username"],
                    "userID": user["userID"],
                    "friends": [],
                },
            )


addDexUsers()

# @app.route("/")
# def home():
#     user = session.get("user")
#     if user:
#         return f"<h2>Logged in as {user['email']}</h2><a href='/logout'>Logout</a>"
#     return '<a href="/login">Login with Dex</a>'


# @app.route("/")
# @app.route("/<path:path>")
# def serve_frontend(path=""):
#     debug_out("serve_frontend")
#     if path != "" and os.path.exists(os.path.join(static_path, path)):
#         return send_from_directory(static_path, path)
#     return send_from_directory(template_path, "index.html")


@app.route("/")
@app.route("/<path:path>")
def home(path=""):
    if isDevEnv:
        return redirect(f"http://localhost:5173")
    else:
        if path != "" and os.path.exists(os.path.join(static_path, path)):
            return send_from_directory(static_path, path)
        return send_from_directory(template_path, "index.html")


@app.route("/login")
def login():
    debug_out("login")
    session["nonce"] = nonce
    redirect_uri = "http://localhost:8000/authorize"
    return oauth.flask_app.authorize_redirect(redirect_uri, nonce=nonce)


@app.route("/authorize")
def authorize():
    token = oauth.flask_app.authorize_access_token()
    nonce = session.get("nonce")

    user_info = oauth.flask_app.parse_id_token(
        token, nonce=nonce
    )  # or use .get('userinfo').json()
    session["user"] = user_info
    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    if isDevEnv:
        return redirect("http://localhost:5173/dashboard")
    return send_from_directory('../frontend/src/Dashboard.svelte', "index.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)


# I have no idea why the dev version requires every fetch/route to start with "/api".
# The production version seems to work fine without it.


@app.route("/api/getinfo")
def getInfo():
    debug_out("getInfo")
    user = session.get("user")
    if user:
        return jsonify({"email": user["email"]})
    return jsonify({"email": None})


@app.route("/api/testfetch")
def testFetch():
    debug_out("testfetch")
    return jsonify({"test": True})


"""POST route to make friend.
Parameters:
    "email" (str): the email of the friend to add
Return codes:
    00: Successfully made friends
    01: User is already friends
    10: User is not logged in
    11: Unable to retrieve user's friendlist
    12: Unable to retrieve friend's friendlist
    13: Friend is the current user
"""
@app.route("/api/post/makefriend", methods=["POST"])
def makeFriends():
    response = {}
    data = request.form
    debug_out("makefriend")
    debug_out(data)

    user = session.get("user")
    if not user:
        return jsonify({"result": 10})

    if user["email"] == data["email"]:
        return jsonify({"result": 13})

    def getCurrFriendList(who):
        doc = mongo.findDocument(DB_USERS, COL_USERS, {"email": who})
        if doc:
            return doc["friends"]
        return None

    user_friends = getCurrFriendList(user["email"])
    friend_friends = getCurrFriendList(data["email"])

    if user_friends is None:
        return jsonify({"result": 11})
    if friend_friends is None:
        return jsonify({"result": 12})

    if data["email"] not in user_friends:
        user_friends.append(data["email"])
        mongo.updateDocument(
            DB_USERS,
            COL_USERS,
            {"friends": user_friends},
            {"email": user["email"]},
        )
    else:
        return jsonify({"result": 1})

    if user["email"] not in friend_friends:
        friend_friends.append(user["email"])
        mongo.updateDocument(
            DB_USERS,
            COL_USERS,
            {"friends": friend_friends},
            {"email": data["email"]},
        )
    return jsonify({"result": 0})
