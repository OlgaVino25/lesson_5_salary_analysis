import requests
from dotenv import load_dotenv
import os

load_dotenv()

SUPER_JOB_CLIENT_ID = os.getenv('SUPER_JOB_ID')
SUPER_JOB_SECRET_KEY = os.getenv('SUPER_JOB_SECRET_KEY')
SUPER_JOB_REDIRECT_URI = os.getenv('SUPER_JOB_REDIRECT_URI')
SUPER_JOB_TOKEN = os.getenv('SUPER_JOB_TOKEN')

BASE_PARAMS = {
    'count': 100,
    'catalogues': '48,33,34,104,173',
}
HEADERS = {
    'X-Api-App-Id': SUPER_JOB_SECRET_KEY,
    'Authorization': f'Bearer {SUPER_JOB_TOKEN}',
}


def find_town_id(town_name: str) -> int:
    """Возвращает ID города по названию используя API SuperJob.

    Args:
        town_name: Название города для поиска

    Returns:
        int: ID города или None, если не найден
    """
    try:
        towns_url = 'https://api.superjob.ru/2.0/towns/'
        response = requests.get(towns_url, headers=HEADERS, params={'all': 1})
        response.raise_for_status()
        towns = response.json()['objects']
        for town in towns:
            if town_name.strip().lower() in town['title'].lower():
                return town['id']
        return None
    except requests.exceptions.RequestException as e:
        print(f'Ошибка при запросе городов: {e}')
        return None
