from mimesis import Person
from mimesis.locales import Locale
import uuid


def generate_first_name():
    return Person(Locale.RU).first_name()


def generate_last_name():
    return Person(Locale.RU).last_name()


def generate_email():
    return Person(Locale.RU).email(domains=["mail.ru"])


users = []

for i in range(1, 11):
    users.append({"id": i, "first_name": generate_first_name(),
                  "last_name": generate_last_name(),
                  "email": generate_email(),
                  "avatar": "https://reqres.in/img/faces/" + str(uuid.uuid4())})

support_data = {
    "url": "https://reqres.in/#support-heading",
    "text": "o keep ReqRes free, contributions towards server costs are appreciated!"
}
