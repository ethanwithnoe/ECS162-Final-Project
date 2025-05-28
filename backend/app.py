from flask import (
    Flask,
    redirect,
    url_for,
    session,
    send_from_directory,
    render_template,
    jsonify,
)
from authlib.integrations.flask_client import OAuth
from authlib.common.security import generate_token
import os

# region Debug Output

# for ease of debugging, debug output will be written to debug_out.txt
DEBUG_FILE = "debug_out.txt"

# clear debug file in startup
with open(DEBUG_FILE, "w") as f:
    f.write("DEBUG LOG\n")


# function to write to debug file
def debug_out(message: str):
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
    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
