import json
from reqres_fast_api.models.User import User

users: list[User] = []

with open("user.json") as f:
    users.extend(json.load(f))
for user in users:
    User.validate(user)
