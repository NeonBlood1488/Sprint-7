import pytest
import allure
import requests
from data import BASE_URL, LOGIN_PATH, ERR_LOGIN_MISSING_FIELD, ERR_ACCOUNT_NOT_FOUND
from helpers import generate_random_string

@allure.feature("Логин курьера")
class TestLoginCourier:

    @allure.title("Успешный логин")
    def test_login_success(self, courier_data):
        login, password, _, _ = courier_data
        payload = {"login": login, "password": password}
        response = requests.post(f"{BASE_URL}{LOGIN_PATH}", data=payload, timeout=20)
        assert response.status_code == 200   # Ожидаем код ответа 200
        assert "id" in response.json()  # И наличие id'шки

    @allure.title("Для логина нужны логин и пароль")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_field_fails(self, missing_field):
        payload = {"login": "test", "password": "123"}
        del payload[missing_field]   # Удаляем одно из обязательных полей
        response = requests.post(f"{BASE_URL}{LOGIN_PATH}", data=payload, timeout=20)
        assert response.status_code == 400   # Ожидаем код ответа 400
        assert response.json().get("message") == ERR_LOGIN_MISSING_FIELD   # И сообщение о неполных данных

    @allure.title("Неверный логин или пароль возвращает ошибку")
    def test_login_invalid_credentials_fails(self, courier_data):
        login, _, _, _ = courier_data
        payload = {"login": login, "password": "wrong"}     # Передаем неверный пароль
        response = requests.post(f"{BASE_URL}{LOGIN_PATH}", data=payload, timeout=20)
        assert response.status_code == 404
        assert response.json().get("message") == ERR_ACCOUNT_NOT_FOUND

    @allure.title("Несуществующий пользователь не может войти")
    def test_login_nonexistent_user_fails(self):
        payload = {"login": generate_random_string(),"password": generate_random_string()}
        response = requests.post(f"{BASE_URL}{LOGIN_PATH}", data=payload, timeout=20)
        assert response.status_code == 404
        assert response.json().get("message") == ERR_ACCOUNT_NOT_FOUND
