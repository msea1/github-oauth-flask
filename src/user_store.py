import json
from dataclasses import asdict, dataclass
from os import stat
from os.path import isfile

USER_STORE_FILE = "users.json"


@dataclass
class UserInfo:
    name: str
    email: str
    tokens: dict[str, str]

    def serialize(self) -> dict:
        return asdict(self)


class DataStore:
    def __init__(self):
        self.cache = self.load_users()

    @staticmethod
    def load_users() -> dict:
        if not isfile(USER_STORE_FILE):
            with open(USER_STORE_FILE, "w"):
                pass  # create an empty file if one does not already exist
        if stat(USER_STORE_FILE).st_size > 0:
            with open(USER_STORE_FILE) as fin:
                return json.load(fin)
        else:
            return {}

    def register_new_user(self, user_name: str, user_email: str, token_src: str, new_token: str) -> None:
        new_user = UserInfo(user_email, user_email, {token_src: new_token})
        self.cache[user_name] = new_user
        self.serialize()

    def serialize(self) -> None:
        dump_info = {key: val.serialize() for key, val in self.cache.items()}
        with open(USER_STORE_FILE, "w") as fout:
            json.dump(dump_info, fout)

    def user_exists(self, user_name: str) -> bool:
        return user_name in self.cache
