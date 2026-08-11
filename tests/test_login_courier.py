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
        with allure.step("Отправить запрос с корректным логином и паролем"):
            payload = {"login": login, "password": password}
            response = requests.post(f"{BASE_URL}{LOGIN_PATH}", data=payload, timeout=20)
        with allure.step("Проверить статус 200 и наличие id"):
            assert response.status_code == 200   # Ожидаем код ответа 200
            assert "id" in response.json()  # И наличие id'шки

    @allure.title("Для логина нужны логин и пароль")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_field_fails(self, missing_field):
        with allure.step(f"Сформировать запрос без поля '{missing_field}'"):
            payload = {"login": "test", "password": "123"}
            del payload[missing_field]   # Удаляем одно из обязательных полей
        with allure.step("Отправить запрос на логин с неполными данными"):
            response = requests.post(f"{BASE_URL}{LOGIN_PATH}", data=payload, timeout=20)
        with allure.step("Проверить статус 400 и сообщение о недостаточности данных"):
            assert response.status_code == 400   # Ожидаем код ответа 400
            assert response.json().get("message") == ERR_LOGIN_MISSING_FIELD   # И сообщение о неполных данных

    @allure.title("Неверный логин или пароль возвращает ошибку")
    def test_login_invalid_credentials_fails(self, courier_data):
        login, _, _, _ = courier_data
        with allure.step("Отправить запрос с верным логином и неверным паролем"):
            payload = {"login": login, "password": "wrong"}     # Передаем неверный пароль
            response = requests.post(f"{BASE_URL}{LOGIN_PATH}", data=payload, timeout=20)
        with allure.step("Проверить статус 404 и сообщение об ошибке"):
            assert response.status_code == 404
            assert response.json().get("message") == ERR_ACCOUNT_NOT_FOUND

    @allure.title("Несуществующий пользователь не может войти")
    def test_login_nonexistent_user_fails(self):
        with allure.step("Сгенерировать несуществующие логин и пароль"):
            payload = {"login": generate_random_string(),"password": generate_random_string()}
        with allure.step("Отправить запрос на логин"):
            response = requests.post(f"{BASE_URL}{LOGIN_PATH}", data=payload, timeout=20)
        with allure.step("Проверить статус 404 и сообщение об отсутствии учётной записи"):
            assert response.status_code == 404
            assert response.json().get("message") == ERR_ACCOUNT_NOT_FOUND
