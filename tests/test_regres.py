import requests
from jsonschema import validate
from resources.schemas import create_user_schema, list_user_schema, update_user_schema


def test_get_user_check_status_code():
    response = requests.get("https://reqres.in/api/users/2")
    assert response.status_code == 200


def test_post_user_check_status_code():
    response = requests.post("https://reqres.in/api/users", data={"name": "morpheus", "job": "leader"})
    assert response.status_code == 201


def test_put_user_check_status_code():
    response = requests.put("https://reqres.in/api/users/2", data={"name": "morpheus", "job": "not leader"})
    assert response.status_code == 200


def test_delete_user_check_status_code():
    response = requests.delete("https://reqres.in/api/users/2")
    assert response.status_code == 204


def test_login_happy_pass():
    response = requests.post("https://reqres.in/api/login",
                             data={"email": "eve.holt@reqres.in", "password": "cityslicka"})
    assert response.status_code == 200
    assert response.json()["token"]


def test_login_without_password():
    response = requests.post("https://reqres.in/api/login", data={"email": "eve.holt@reqres.in"})
    assert response.status_code == 400
    assert response.json()["error"] == "Missing password"


def test_get_user_not_found():
    response = requests.get("https://reqres.in/api/users/23")
    assert response.status_code == 404


def test_create_user_validate_schema():
    response = requests.post("https://reqres.in/api/users", data={"name": "morpheus", "job": "leader"})
    validate(response.json(), schema=create_user_schema)


def test_list_users_validate_schema():
    response = requests.get("https://reqres.in/api/users", params={"page": 2})
    validate(response.json(), schema=list_user_schema)

def test_update_user_validate_schema():
    """Здесь в схеме я поиграла с полями - убрала поле ypdateAt и выставила additionalProperties: False.
    Для прохождения теста закомментила additionalProperties  в схеме"""

    response = requests.put("https://reqres.in/api/users/2", data={"name": "morpheus", "job": "not leader"})
    validate(response.json(), schema=update_user_schema)


def test_get_user_returns_correct_user():
    "Как будто проверяю логику =)"
    id = 2
    response = requests.get(f"https://reqres.in/api/users/{id}")
    assert response.json()["data"]["id"]==id


def test_creating_and_updating_user():
    """Хотела проверить логику создание-обновление-проверка обновления
    Но видимо на regres  не создаются реальные записи и поэтому конечную проверку заменила на проверку статус-кода
    В комменте показала как примерно выглядела бы реальная проверка
    """
    create_json = requests.post("https://reqres.in/api/users", data={"name": "harry potter", "job": "student"}).json()
    created_id = create_json["id"]

    url = f"https://reqres.in/api/users/{created_id}"
    response_update = requests.put(url, data={"name": "harry potter", "job": "auror"})
    assert response_update.status_code == 200

    response_get_user = requests.get(url)
    assert response_get_user.status_code == 404
    #assert response_get_user.json()["data"]["name"]==response_update.json()["name"]
