import requests


def find_hh_town_id(city_name, headers):
    """Возвращает ID города по названию используя API HeadHunter."""
    areas_url = 'https://api.hh.ru/areas'
    response = requests.get(areas_url, headers=headers)
    response.raise_for_status()

    if not city_name or not city_name.strip():
        print("Неверное название города")
        return None

    normalized_city = city_name.strip().lower()
    countries = response.json()

    if not countries:
        print("Пустой ответ от API")
        return None
    
    while countries:
        area = countries.pop()
        
        if 'name' not in area:
            continue
            
        if area['name'].lower() == normalized_city:
            return area['id']
        
        if area.get('areas'):
            countries.extend(area['areas'])
    
    print(f"Город '{city_name}' не найден")
    return None
