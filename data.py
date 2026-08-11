BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"  # Базовый URL API

# Эндпоинты
COURIER_PATH = "/courier"
LOGIN_PATH = "/courier/login"
ORDERS_PATH = "/orders"

# Ожидаемые сообщения об ошибках (сверены с документацией)
ERR_CREATE_MISSING_FIELD = "Недостаточно данных для создания учетной записи"
ERR_LOGIN_MISSING_FIELD = "Недостаточно данных для входа"
ERR_ACCOUNT_NOT_FOUND = "Учетная запись не найдена"
ERR_COURIER_NOT_FOUND = "Курьер с идентификатором {courierId} не найден"
ERR_LOGIN_ALREADY_USED = "Этот логин уже используется. Попробуйте другой."
