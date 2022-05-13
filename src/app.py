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


def create_app(_config_filename: str) -> Flask:
    app = Flask(__name__)
    # app.config.from_pyfile(config_filename)

    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"

    return app
