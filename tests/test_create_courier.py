import pytest
import allure
import requests
from data import BASE_URL, COURIER_PATH, ERR_CREATE_MISSING_FIELD, ERR_LOGIN_ALREADY_USED
from helpers import create_courier, generate_random_string, login_courier, delete_courier

@allure.feature("Создание курьера")
class TestCreateCourier:

    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self):
        login, password, first_name, response = create_courier()
        assert response.status_code == 201
        assert response.json() == {"ok": True}
        courier_id = login_courier(login, password)
        delete_courier(courier_id)

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier_fails(self):
        login, password, first_name, _ = create_courier()   # Пытаемся создать второго с теми же данными
        _, _, _, response2 = create_courier(login=login, password=password, first_name=first_name)
        assert response2.status_code == 409   # Ждём-с ответ 409
        assert response2.json().get("message") == ERR_LOGIN_ALREADY_USED  # И ошибку
        courier_id = login_courier(login, password)
        delete_courier(courier_id)

    @allure.title("Обязательные поля (логин и пароль) должны присутствовать")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_field_fails(self, missing_field):
        data = {"login": generate_random_string(),"password": generate_random_string(),"firstName": generate_random_string()}
        del data[missing_field]   # Удаляем одно из обязательных полей
        response = requests.post(f"{BASE_URL}{COURIER_PATH}", data=data)
        assert response.status_code == 400     # Ожидаем ответ 400
        assert response.json().get("message") == ERR_CREATE_MISSING_FIELD   # И сообщение об ошибке

    @allure.title("Успешный запрос возвращает ok: true")
    def test_create_courier_returns_ok(self):
        login, password, first_name, response = create_courier()
        assert response.json() == {"ok": True}   # Проверяем только поле ok, т.к. статус уже проверен ранее
        courier_id = login_courier(login, password)
        delete_courier(courier_id)
