import pytest
import allure
import requests
from data import BASE_URL, ORDERS_PATH

@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.title("Проверка создания заказа с разными вариантами цвета")
    @pytest.mark.parametrize("colors", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ], ids=["black", "grey", "both", "none"])
    def test_create_order_colors(self, colors):
        payload = {
            "firstName": "Иван",
            "lastName": "Петров",
            "address": "ул. Ленина, 1",
            "metroStation": 1,
            "phone": "+79998887766",
            "rentTime": 1,
            "deliveryDate": "2025-12-31",
            "comment": "Тест",
            "color": colors}
        response = requests.post(f"{BASE_URL}{ORDERS_PATH}", json=payload)
        assert response.status_code == 201
        assert "track" in response.json()
        assert isinstance(response.json()["track"], int)
