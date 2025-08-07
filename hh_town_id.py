import requests
from dotenv import load_dotenv
import os

load_dotenv()

HH_ACCESS_TOKEN = os.getenv('HH_ACCESS_TOKEN')
YANDEX_LOGIN = os.getenv('YANDEX_LOGIN')

HEADERS = {
    'Authorization': f'Bearer {HH_ACCESS_TOKEN}',
    'User-Agent': 'MyHHIntegration/1.0 ({YANDEX_LOGIN})'
}


def find_hh_town_id(town_name: str) -> int:
    """Возвращает ID города по названию используя API HeadHunter.

    Args:
        town_name: Название города для поиска

    Returns:
        int: ID города или None, если не найден
    """
    try:
        areas_url = 'https://api.hh.ru/areas'
        response = requests.get(areas_url, headers=HEADERS)
        response.raise_for_status()
        countries = response.json()

        for country in countries:
            if town_name.strip().lower() == country['name'].lower():
                return country['id']

            if 'areas' in country:
                for region in country['areas']:
                    if town_name.strip().lower() == region['name'].lower():
                        return region['id']

                    if 'areas' in region:
                        for city in region['areas']:
                            if town_name.strip().lower() == city['name'].lower():
                                return city['id']
        return None
    except requests.exceptions.RequestException as e:
        print(f'Ошибка при запросе городов: {e}')
        return None
