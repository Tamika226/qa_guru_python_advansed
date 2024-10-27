from reqres_tests.models.users import User


def test_create_user(user_client):
    expected_new_user = User(first_name="Adam", last_name="Smith", email="john@example.com",
                             avatar="https://reqres.in/img/faces/2-image.jpg")
    new_user = user_client.create_user(expected_new_user)

    assert new_user.email == expected_new_user.email
    assert new_user.last_name == expected_new_user.last_name
    assert new_user.first_name == expected_new_user.first_name
    assert new_user.avatar == expected_new_user.avatar


def test_get_users(user_client):
    all_users = user_client.get_users()
    assert len(all_users.items) > 0
    assert all_users.total == len(all_users.items)


def test_get_user(user_client):
    expected_response_get_user = User(email="abby.lindon@reqres.in",
                                      first_name="Abby",
                                      last_name="Lindon",
                                      avatar="https://reqres.in/img/faces/1-image.jpg")
    user = user_client.get_user(2)

    assert user.email == expected_response_get_user.email
    assert user.first_name == expected_response_get_user.first_name
    assert user.last_name == expected_response_get_user.last_name
    assert user.avatar == expected_response_get_user.avatar
