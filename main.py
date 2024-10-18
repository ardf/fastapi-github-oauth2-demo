import os
from fastapi import FastAPI, Request
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from starlette.templating import Jinja2Templates

GITHUB_CLIENT_ID = os.environ.get("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.environ.get("GITHUB_CLIENT_SECRET")

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="APP_SECRET_KEY")

config = Config(
    environ={
        "GITHUB_CLIENT_ID": GITHUB_CLIENT_ID,
        "GITHUB_CLIENT_SECRET": GITHUB_CLIENT_SECRET,
    }
)
oauth = OAuth(config)
oauth.register(
    name="github",
    client_id=GITHUB_CLIENT_ID,
    client_secret=GITHUB_CLIENT_SECRET,
    authorize_url="https://github.com/login/oauth/authorize",
    authorize_params=None,
    access_token_url="https://github.com/login/oauth/access_token",
    access_token_params=None,
    userinfo_endpoint="https://api.github.com/user",
    client_kwargs={"scope": "user:email"},
)

templates = Jinja2Templates(directory="templates")


class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email


# Index route: Homepage with GitHub Sign-in button
@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# GitHub OAuth Sign-in endpoint
@app.get("/login")
async def login_via_github(request: Request):
    redirect_uri = request.url_for("auth")
    return await oauth.github.authorize_redirect(request, redirect_uri)


# Callback URL to handle GitHub response
@app.route("/auth")
async def auth(request: Request):
    token = await oauth.github.authorize_access_token(request)
    # Fetch user info from GitHub API using the access token
    user_data = await oauth.github.get("https://api.github.com/user", token=token)
    user_data = user_data.json()

    user = User(username=user_data["login"], email=user_data["email"])

    return templates.TemplateResponse(
        "profile.html", {"request": request, "user": user}
    )
