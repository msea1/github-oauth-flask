import json

import requests

USER_REPO_INFO_API = "https://api.github.com/users/{}/repos"
PULL_REQUEST_INFO_API = "https://api.github.com/search/issues?q=+type:pr+state:open+user:{}"


def get_repo_info_from_user(user_login: str) -> dict:
    resp = requests.get(USER_REPO_INFO_API.format(user_login))
    return json.loads(resp.content)  # TODO: document sample reply from GH API


def get_pull_req_counts(user_login: str) -> dict:
    try:
        resp = requests.get(PULL_REQUEST_INFO_API.format(user_login))
        data = json.loads(resp.content)  # TODO: document sample reply from GH API
        pulls = data["items"]
    except Exception as exc:
        print(f"error pulling pull request data: {exc}")
        return {}
    counts = {}
    for pull in pulls:
        repo_name = pull["repository_url"].split("/")[-1]
        if repo_name not in counts:
            counts[repo_name] = 0
        counts[repo_name] += 1
    return counts
