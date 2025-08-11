import requests


def find_hh_town_id(city_name, headers):
    """Возвращает ID города по названию используя API HeadHunter.

    Args:
        town_name: Название города для поиска

    Returns:
        int: ID города или None, если не найден
    """
    areas_url = 'https://api.hh.ru/areas'
    response = requests.get(areas_url, headers=headers)
    response.raise_for_status()
    countries = response.json()

    for country in countries:
        if city_name.strip().lower() == country['name'].lower():
            return country['id']

        if 'areas' in country:
            for region in country['areas']:
                if city_name.strip().lower() == region['name'].lower():
                    return region['id']

                if 'areas' in region:
                    for city in region['areas']:
                        if city_name.strip().lower() == city['name'].lower():
                            return city['id']
    return None
