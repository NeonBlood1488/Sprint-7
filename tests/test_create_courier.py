import pytest
import allure
import requests
from data import BASE_URL, COURIER_PATH, ERR_CREATE_MISSING_FIELD, ERR_LOGIN_ALREADY_USED
from helpers import create_courier, generate_random_string, login_courier, delete_courier

@allure.feature("Создание курьера")
class TestCreateCourier:
    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self):
        with allure.step("Создать курьера с уникальными данными"):
            login, password, first_name, response = create_courier()
        with allure.step("Проверить статус ответа 201 и поле ok=true"):
            assert response.status_code == 201
            assert response.json() == {"ok": True}
        with allure.step("Очистить данные: удалить курьера"):
            courier_id = login_courier(login, password)
            delete_courier(courier_id)

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier_fails(self):
        with allure.step("Создать первого курьера"):
            login, password, first_name, _ = create_courier()   # Пытаемся создать второго с теми же данными
        with allure.step("Попытаться создать второго курьера с теми же логином и паролем"):
            _, _, _, response2 = create_courier(login=login, password=password, first_name=first_name)
        with allure.step("Проверить ответ: статус 409 и сообщение о занятом логине"):
            assert response2.status_code == 409   # Ждем-с ответ 409
            assert response2.json().get("message") == ERR_LOGIN_ALREADY_USED  # И ошибку
        with allure.step("Очистить данные: удалить первого курьера"):
            courier_id = login_courier(login, password)
            delete_courier(courier_id)

    @allure.title("Обязательные поля (логин и пароль) должны присутствовать")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_field_fails(self, missing_field):
        with allure.step(f"Сформировать данные без поля '{missing_field}'"):
            data = {"login": generate_random_string(),"password": generate_random_string(),"firstName": generate_random_string()}
            del data[missing_field]   # Удаляем одно из обязательных полей
        with allure.step("Отправить запрос на создание курьера с неполными данными"):
            response = requests.post(f"{BASE_URL}{COURIER_PATH}", data=data)
        with allure.step("Проверить ответ: статус 400 и сообщение об ошибке"):
            assert response.status_code == 400     # Ожидаем код ответа 400
            assert response.json().get("message") == ERR_CREATE_MISSING_FIELD   # И сообщение об ошибке

    @allure.title("Успешный запрос возвращает ok: true")
    def test_create_courier_returns_ok(self):
        with allure.step("Создать курьера"):
            login, password, first_name, response = create_courier()
        with allure.step("Проверить, что тело ответа содержит ok=true"):
            assert response.json() == {"ok": True}   # Проверяем только поле ok, т.к. статус уже проверен ранее
        with allure.step("Очистить данные: удалить курьера"):
            courier_id = login_courier(login, password)
            delete_courier(courier_id)
