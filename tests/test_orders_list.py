import allure
import requests
from data import BASE_URL, ORDERS_PATH

@allure.feature("Список заказов")
class TestOrdersList:

    @allure.title("Тело ответа содержит список заказов")
    def test_orders_list_returns_list(self):
        response = requests.get(f"{BASE_URL}{ORDERS_PATH}")
        assert response.status_code == 200
        data = response.json()
        assert "orders" in data
        assert isinstance(data["orders"], list)
        if data["orders"]:                           # Проверка структуры первого заказа, если есть
            first = data["orders"][0]
            assert "id" in first
            assert "courierId" in first
            assert "track" in first
            assert "color" in first
