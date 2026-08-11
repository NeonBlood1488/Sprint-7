import random
import string
import requests
from data import BASE_URL, COURIER_PATH, LOGIN_PATH

def generate_random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def create_courier(login=None, password=None, first_name=None):
    login = login or generate_random_string(10)
    password = password or generate_random_string(10)
    first_name = first_name or generate_random_string(10)
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name}
    response = requests.post(f"{BASE_URL}{COURIER_PATH}", data=payload)
    return login, password, first_name, response

def login_courier(login, password):
    payload = {"login": login, "password": password}
    response = requests.post(f"{BASE_URL}{LOGIN_PATH}", data=payload)
    if response.status_code == 200:
        return response.json().get("id")
    return None

def delete_courier(courier_id):
    if courier_id is None:
        return
    response = requests.delete(f"{BASE_URL}{COURIER_PATH}/{courier_id}")
    return response
