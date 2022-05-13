from os import getenv
from uuid import uuid4

import requests
from flask import Flask

"""
- Setup a basic [Flask](https://flask.palletsprojects.com/en/2.0.x/) server that can handle the [Github OAuth web application login 
flow](https://docs.github.com/en/developers/apps/building-oauth-apps/authorizing-oauth-apps)
    - After callback, require the user to provide an activation code
    - When the user provides the correct activation code `OCTOCAT`, create a `User` object for them to store their Github email, 
    Github username, and Github access token.
    - Store their Github username in a session cookie.
    - Redirect to a page that shows a list of their public repos with name, organization, # stars, and # of PRs. ([Repo API](
    https://docs.github.com/en/rest/reference/repos#list-repositories-for-the-authenticated-user))
- Setup a basic frontend with the three relevant pages:
    1. Display the login button to logged out users
    2. After the OAuth redirect, page to request an activation code from the user
    3. After activation code is collected, display a table with the user's public repos.
"""


def create_app() -> Flask:
    app = Flask(__name__)
    app.config['CLIENT_ID'] = getenv("GITHUB_CLIENT_ID", "default_client")
    app.config['CLIENT_SECRET'] = getenv("GITHUB_CLIENT_SECRET", "default_secret")

    @app.route("/")
    def index():
        secret_key = app.config.get("CLIENT_SECRET")
        return f"Found {secret_key}"

    @app.route("/github-login")
    def github_login():
        payload = {'client_id': app.config.get("CLIENT_ID"), 'state': uuid4().hex}
        r = requests.get('https://github.com/login/oauth/authorize', params=payload)
        return r.content

    @app.route("/github-callback")
    def github_callback():
        return "Called by github!"

    return app
