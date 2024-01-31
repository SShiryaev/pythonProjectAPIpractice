import json
import os

import requests


from src.config import API_KEY


def get_currency_rate(base: str) -> float:
    """Получает курс рубля по API и возвращает его в виде float."""

    url = "https://api.apilayer.com/exchangerates_data/latest"

    response = requests.get(url, headers={'apikey': API_KEY}, params={'base': base})
    rate = response.json()['rates']['RUB']
    return rate


def save_to_json(data: dict, json_file) -> None:
    """Сохраняет данные в json файл."""

    with open(os.path.join(json_file), 'a') as j_file:
        if os.stat(json_file).st_size == 0:
            json.dump([data], j_file)
        else:
            with open(json_file) as file:
                data_list = json.load(file)
            data_list.append(data)
            with open(json_file, "w") as file:
                json.dump(data_list, file)


def get_read_json(json_file) -> dict:
    """Берет данные из json файла и возвращает их."""

    with open(json_file, 'r', encoding="utf-8") as file:
        data = json.load(file)
    return data
