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
import requests
from datetime import datetime, timezone, timedelta

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
        try:
            with open(DEBUG_FILE, "a") as f:
                f.write(str(message) + "\n")
        except Exception as e:
            print("Debug write failed:", e)


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
# Database and collection names
DB_FOOD = "fooddb"
COL_FOOD = "food"
DB_USERS = "usersdb"
COL_USERS = "users"


# Function to add Dex accounts to Database
# This is hardcoded, it is not synced with Dex.
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

# region Dex


@app.route("/login")
def login():
    # debug_out("login")
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
    return send_from_directory(template_path, "index.html")


@app.route("/meals")
def meals():
    if isDevEnv:
        return redirect("http://localhost:5173/meals")
    return send_from_directory("../frontend/src/Meals.svelte", "index.html")


@app.route("/goals")
def goals():
    if isDevEnv:
        return redirect("http://localhost:5173/goals")
    return send_from_directory("../frontend/src/Goals.svelte", "index.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# endregion Dex


# I have no idea why the dev version requires every fetch/route to start with "/api".
# The production version seemed to work fine without it.


# Route to get the current session's user info
# currently just returns email, but more might be added later
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


# region Friends


# POST route to make friend.
# Parameters:
#     "email" (str): the email of the friend to add
# Return codes:
#     00: Successfully made friends
#     01: User is already friends
#     10: User is not logged in
#     11: Unable to retrieve user's friendlist
#     12: Unable to retrieve friend's friendlist
#     13: Friend is the current user
@app.route("/api/post/makefriend", methods=["POST"])
def makeFriends():
    response = {}
    data = request.form
    debug_out("makefriend")
    debug_out(data)

    # check that user is logged in
    user = session.get("user")
    if not user:
        return jsonify({"result": 10})

    # check if trying to make friends with self
    if user["email"] == data["email"]:
        return jsonify({"result": 13})

    # get friends list for both parties
    def getCurrFriendList(who):
        doc = mongo.findDocument(DB_USERS, COL_USERS, {"email": who})
        if doc:
            return doc["friends"]
        return None

    user_friends = getCurrFriendList(user["email"])
    friend_friends = getCurrFriendList(data["email"])

    # check if failed to get either friendlist
    if user_friends is None:
        return jsonify({"result": 11})
    if friend_friends is None:
        return jsonify({"result": 12})

    # add friend
    if data["email"] not in user_friends:
        user_friends.append(data["email"])
        mongo.updateDocument(
            DB_USERS,
            COL_USERS,
            {"friends": user_friends},
            {"email": user["email"]},
        )
    else:
        # already friends
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


# POST route to remove friend.
# Parameters:
#     "email" (str): the email of the friend to remove
# Return codes:
#     00: Successfully removed friend
#     01: User is already not friends
#     10: User is not logged in
#     11: Unable to retrieve user's friendlist
#     12: Unable to retrieve friend's friendlist
#     13: Friend is the current user
@app.route("/api/post/removefriend", methods=["POST"])
def removeFriends():
    response = {}
    data = request.form
    debug_out("removefriend")
    debug_out(data)

    # check that user is logged in
    user = session.get("user")
    if not user:
        return jsonify({"result": 10})

    # check if trying to unfriend themself
    if user["email"] == data["email"]:
        return jsonify({"result": 13})

    # get friends list for both parties
    def getCurrFriendList(who):
        doc = mongo.findDocument(DB_USERS, COL_USERS, {"email": who})
        if doc:
            return doc["friends"]
        return None

    user_friends = getCurrFriendList(user["email"])
    friend_friends = getCurrFriendList(data["email"])

    # check if failed to get either friendlist
    if user_friends is None:
        return jsonify({"result": 11})
    if friend_friends is None:
        return jsonify({"result": 12})

    # remove friend
    if data["email"] in user_friends:
        user_friends.remove(data["email"])
        mongo.updateDocument(
            DB_USERS,
            COL_USERS,
            {"friends": user_friends},
            {"email": user["email"]},
        )
    else:
        # already not friends
        return jsonify({"result": 1})

    if user["email"] in friend_friends:
        friend_friends.remove(user["email"])
        mongo.updateDocument(
            DB_USERS,
            COL_USERS,
            {"friends": friend_friends},
            {"email": data["email"]},
        )

    return jsonify({"result": 0})


# GET route to get friends list.
# Return codes:
#     00: Successfully retrieved user's friendlist
#     10: User is not logged in
#     11: Unable to retrieve user's friendlist
@app.route("/api/get/friendslist")
def getFriendsList():
    # check that user is logged in
    user = session.get("user")
    if not user:
        return jsonify({"result": 10})

    # get friends list for both parties
    def getCurrFriendList(who):
        doc = mongo.findDocument(DB_USERS, COL_USERS, {"email": who})
        if doc:
            return doc["friends"]
        return None

    user_friends = getCurrFriendList(user["email"])
    # check if failed to get either friendlist
    if user_friends is None:
        return jsonify({"result": 11})

    friendsList = []
    extras = []
    for friend_email in user_friends:
        doc = mongo.findDocument(DB_USERS, COL_USERS, {"email": friend_email})
        if doc:
            friendsList.append((friend_email, doc["username"]))
        else:
            extras.append((friend_email, "Unknown User"))

    friendsList.sort(key=lambda x: x[1])  # sort by username
    extras.sort(key=lambda x: x[0])  # sort by email
    friendsList.extend(extras)
    return jsonify({"result": 0, "friendsList": friendsList})


# endregion Friends


# Production Mode requires this be last.
# This seems not the case for Dev Mode.
@app.route("/")
@app.route("/<path:path>")
def home(path=""):
    if isDevEnv:
        return redirect(f"http://localhost:5173")
    else:
        if path != "" and os.path.exists(os.path.join(static_path, path)):
            return send_from_directory(static_path, path)
        return send_from_directory(template_path, "index.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)

# region Food Tracking

USDA_API_KEY = os.getenv("USDA_API_KEY")

# This can fail if the url gets blocked by your VPN


@app.route("/api/search", methods=["GET"])
def search():
    query = request.args.get("query")
    if query is None:
        return jsonify({"error": "no query"}), 400

    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key={USDA_API_KEY}&query={query}"
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({"error": "error"}), 500

    data = response.json()
    return jsonify(data), 200


@app.route("/api/addfood", methods=["POST"])
def addfood():
    data = request.json
    data["userid"] = session.get("user", {}).get("email", "INVALID")
    data["timestamp"] = datetime.now(timezone.utc).isoformat()

    result = mongo.insertDocument(DB_FOOD, COL_FOOD, data)

    return (
        jsonify(
            {
                # add brand name and useid and timestamp
                "userid": data.get("userid"),
                "timestamp": data.get("timestamp"),
                "brand": data.get("brand"),
                "name": data.get("name"),
                "calories": data.get("calories"),
                "protein": data.get("protein"),
                "fat": data.get("fat"),
                "carbohydrates": data.get("carbohydrates"),
                "inserted_id": str(result.inserted_id),
            }
        ),
        201,
    )


# GET route to get user's logged foods.
# Query:
#     range (Optional): One of "today", "week", "month", or "custom"
#       Specifies the time range to filter foods from.
#       If not one of the above values or not specified, defaults to show all foods.
#     earliest (Optional): a date (UTC) in YYYY-MM-DD format
#       When range is set to "custom", defines the lower bound of the filtered time range
#       If not specified, the time range will be unbonded.
#     latest (Optional): a date (UTC) in YYYY-MM-DD format
#       When range is set to "custom", defines the upper bound of the filtered time range
#       If not specified, the time range will be unbonded.
# Return codes:
#     00: Successfully retrieved user's logged foods
#     10: User is not logged in
@app.route("/api/getuserfoods", methods=["GET"])
def getUserFoods():
    # check that user is logged in
    user = session.get("user")
    if not user:
        return jsonify({"result": 10})

    # define time range
    latest = None
    earliest = None

    timeRange = request.args.get("range")
    if timeRange == "custom":
        arg_earliest = request.args.get("earliest")
        arg_latest = request.args.get("latest")

        if arg_earliest:
            earliest = datetime.fromisoformat(arg_earliest)
            earliest = earliest.replace(tzinfo=timezone.utc)
        if arg_latest:
            latest = datetime.fromisoformat(arg_latest)
            latest = latest.replace(tzinfo=timezone.utc)

    elif timeRange == "today":
        latest = datetime.now(timezone.utc)  # now
        earliest = latest - timedelta(days=1)
    elif timeRange == "week":
        latest = datetime.now(timezone.utc)  # now
        earliest = latest - timedelta(days=7)
    elif timeRange == "month":
        latest = datetime.now(timezone.utc)  # now
        earliest = latest - timedelta(days=30)
    else:
        pass

    # get all foods logged by the user
    docs = mongo.searchDocument(DB_FOOD, COL_FOOD, {"userid": user["email"]})

    foodList = []

    # search through foods
    for doc in docs:
        # check if within the specified timeframe
        timestamp = datetime.fromisoformat(doc["timestamp"])
        # return {"e":earliest,"t":timestamp}
        if (earliest is None or timestamp > earliest) and (
            latest is None or timestamp < latest
        ):
            jsonDoc = doc.copy()
            # convert ObjectID to string
            jsonDoc["_id"] = str(jsonDoc["_id"])
            foodList.append(jsonDoc)
    return jsonify({"result": 0, "foodList": foodList})


# endregion Food Tracking
