import datetime

user = {
    "id": int,
    "email": str,
    "first_name": str,
    "last_name": str,
    "avatar": str,
}

support = {
    "url": str,
    "text": str,
}

user_get = {
    "data": user,
    "support": support
}

all_users_get ={
    "page": int,
    "per_page": int,
    "total": int,
    "total_pages": int,
    "data": [user],
    "support": support
}

new_user = {
    "name": str,
    "job": str
}

created_user = {
    "name": str,
    "job": str,
    "id": int,
    "createdAt": str
}

update_user = {
    "name": str,
    "job": str,
    "updatedAt": str
}

