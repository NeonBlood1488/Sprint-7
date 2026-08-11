import pytest
from helpers import create_courier, login_courier, delete_courier

@pytest.fixture
def courier_data():
    login, password, first_name, response = create_courier()  # Создаем курьера
    assert response.status_code == 201, f"Не удалось создать курьера: {response.text}"
    courier_id = login_courier(login, password)     # Логинимся, чтобы получить id
    assert courier_id is not None, "Не удалось получить id курьера"
    yield login, password, first_name, courier_id  # Передача данных в тест
    delete_courier(courier_id)    # Удаляем курьера после теста
