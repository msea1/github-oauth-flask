import pprint
from os import getenv

from flask import Flask, redirect, render_template_string, request, session, url_for
from flask_oauthlib.client import OAuth

from src.github_api import get_pull_req_counts, get_repo_info_from_user
from src.js_fx import activation_code_js_validator
from src.user_store import DataStore

""" TODOs
hash the github tokens
replace user store with sqlite; maintain an in-memory cache
create templates for each page and style content
add unit tests
"""


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = getenv("APP_SECRET_KEY", "fake_secret")
    app.config["CLIENT_ID"] = getenv("GITHUB_CLIENT_ID", "fake_id")
    app.config["CLIENT_SECRET"] = getenv("GITHUB_CLIENT_SECRET", "fake_secret")
    app.config["USERS"]: DataStore = DataStore()

    oauth = OAuth(app)
    oauth.init_app(app)
    github = oauth.remote_app(  # nosec
        "github",
        consumer_key=app.config.get("CLIENT_ID"),
        consumer_secret=app.config.get("CLIENT_SECRET"),
        base_url="https://api.github.com/",
        request_token_url=None,
        access_token_method="POST",
        access_token_url="https://github.com/login/oauth/access_token",
        authorize_url="https://github.com/login/oauth/authorize",
    )

    @github.tokengetter
    def get_github_token():
        return session.get("github_token")

    @app.route("/")
    def index():
        # Basic front-end page 1: Display the login button to logged out users
        if "github_token" in session:
            # already logged in, go to the repo display page
            return redirect(url_for("display"))
        return """<html>
        <input type='button' style="background:#3366CC;color:white;" id='login' 
        onclick='location.href="/login"' value='Log in with Github'>
        <html>"""

    @app.route("/login")
    def github_login():
        # redirect to github oauth and then head to /login/authorized
        cb = url_for("authorized", _external=True, _scheme="https")
        return github.authorize(callback=cb)

    @app.route("/login/authorized")
    def authorized():
        resp = github.authorized_response()
        if resp is None:
            session.clear()
            message = (
                f"Access denied: reason={request.args['error']} "
                f"error={request.args['error_description']} "
                f"full={pprint.pformat(request.args)}"
            )
        else:
            try:
                session["github_token"] = (resp["access_token"], "")
                session["user_data"] = github.get("user").data
                seen_before = app.config["USERS"].user_exists(session["user_data"]["login"])
                if seen_before:
                    return redirect(url_for("display"))
                return activate()
            except Exception as exc:
                session.clear()
                message = f"Unable to login, please try again.<br/><br/>{exc}"
        return f"<html><p>{message}</p></html>"

    @app.route("/activate")
    def activate():
        # Basic front-end page 2: After the OAuth redirect, page to request an activation code from the user
        return render_template_string(
            f"""
            <div><input type="text" id="input_code" name="input_code" placeholder="activation code"></div>
            <div><button style="background:#3366CC;color:white;" onclick="check_code()">Complete sign up</button></div>
            {activation_code_js_validator()}
            """
        )

    @app.route("/register-user")
    def register_user():
        user_name, user_email, access_token = (
            session["user_data"]["login"],
            session["user_data"]["email"],
            session["github_token"],
        )
        app.config["USERS"].register_new_user(user_name, user_email, "GitHub", access_token)
        return redirect(url_for("display"))

    @app.route("/info")
    def display():
        # Basic front-end page 3. After activation code is collected, display a table with the user's public repos.
        return render_template_string(
            f"""
            <div><input type='button' style='background:#3366CC;color:white;' id='logout'
                onclick='location.href="/logout"' value='Logout'></div>
            <div>{show_repos()}</div>
        """
        )

    @app.route("/show-repos")
    def show_repos():
        user_login = session["user_data"]["login"]
        json_list = get_repo_info_from_user(user_login)
        pr_counts = get_pull_req_counts(user_login)

        # iterate through repo info and pull out desired info: name, org, stars, # PRs
        pruned_data = [
            f"""<tr>
            <td>{repo["name"]}</td>
            <td><a href='{repo['owner']['url']}' target='new'>{repo['owner']['login']}</td>
            <td>{repo["stargazers_count"]}</td>
            <td>{pr_counts.get(repo["name"], 0)}</td></tr>
        """
            for repo in json_list
        ]
        as_table = "".join(pruned_data)
        return f"""Your repos<br/><table>
        <tr>
            <th>Name</th>
            <th>Organization</th>
            <th>Stars</th>
            <th>#PRs</th>
        </tr>
        {as_table}
        </table>
        """

    @app.route("/logout")
    def logout():
        session.clear()
        return "<html><p>You were logged out!</p></html>"

    return app
