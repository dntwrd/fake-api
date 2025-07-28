import requests
import json

def test_search():
    env = "http://127.0.0.1:8000"
    requst  = "/search"

    url = env + requst

    params = {
        "city": "Санкт-Петербург",
        "check_in": "2025-11-30",
        "check_out": "2025-12-30"
    }

    response = requests.post(url, params=params)
    json_resp = json.loads(response.text)

    print("\n###")
    print(json_resp['code'])
    print("###")

    print("Проверка http кода")
    if response.status_code == 200:
        print("Проверка http кода прошла успешно")
    else:
        raise AssertionError(f"Статус код неверен: {response.status_code}")
    print("Проверка кода ошибки")
    assert json_resp['code'] == 115515