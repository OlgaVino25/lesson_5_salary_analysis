import requests


BASE_PARAMS = {
    'count': 100,
    'catalogues': '48,33,34,104,173',
}


def find_town_id(city_name, headers):
    """Возвращает ID города по названию используя API SuperJob.

    Args:
        town_name: Название города для поиска

    Returns:
        int: ID города или None, если не найден
    """
    towns_url = 'https://api.superjob.ru/2.0/towns/'
    response = requests.get(towns_url, headers=headers, params={'all': 1})
    response.raise_for_status()
    towns = response.json()['objects']
    for town in towns:
        if city_name.strip().lower() in town['title'].lower():
            return town['id']
    return None
