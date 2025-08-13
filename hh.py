import requests
from salary_utils import calculate_stats
from hh_town_id import find_hh_town_id


def fetch_hh_page(page, language_query, area_id, hh_headers):
    """Выполняет запрос к HeadHunter API для конкретной страницы.
    
    Args:
        page (int): Номер страницы для запроса
        language_query (str): Язык программирования для поиска
        area_id (int): ID региона (города) для поиска
        hh_headers (dict): Заголовки для запроса к API HeadHunter

    Returns:
        dict: JSON-ответ от API с вакансиями
    """
    response = requests.get(
        'https://api.hh.ru/vacancies',
        headers=hh_headers,
        params={
            'text': language_query,
            'area': area_id,
            'per_page': 100,
            'page': page
        },
        timeout=10
    )
    response.raise_for_status()
    return response.json()


def fetch_hh_vacancies(language_query, area_id, hh_headers):
    """Получает все вакансии по языку программирования и региону.

    Args:
        language_query (str): Язык программирования для поиска
        area_id (int): ID региона (города) для поиска
        hh_headers (dict): Заголовки для запроса к API HeadHunter

    Returns:
        tuple: Кортеж из двух элементов:
            - list: Список вакансий
            - int: Общее количество найденных вакансий (из API)
    """
    all_vacancies = []
    page = 0
    max_attempts = 3
    total_found = 0
    
    try:
        initial_page = fetch_hh_page(0, language_query, area_id, hh_headers)
        total_found = initial_page['found']
        total_pages = initial_page.get('pages', 0)
        all_vacancies.extend(initial_page.get('items', []))
        page = 1
    except requests.exceptions.RequestException as e:
        print(f'Ошибка при загрузке первой страницы: {e}')
        total_pages = 0

    while page < total_pages:
        attempts = 0
        success = False
        
        while attempts < max_attempts and not success:
            try:
                current_page = fetch_hh_page(page, language_query, area_id, hh_headers)
                all_vacancies.extend(current_page.get('items', []))
                success = True
            except requests.exceptions.RequestException as e:
                attempts += 1
                if attempts < max_attempts:
                    print(f'Повторная попытка ({attempts}/{max_attempts}) для страницы {page}...')
                else:
                    print(f'Ошибка при загрузке страницы {page} после {max_attempts} попыток: {e}')
        page += 1

    return all_vacancies, total_found


def get_hh_statistics(city_name, hh_headers, languages):
    """Получает статистику по зарплатам для всех языков программирования.

    Args:
        city_name (str): Название города для поиска
        hh_headers (dict): Заголовки для запроса к API HeadHunter
        languages (list): Список языков программирования для анализа

    Returns:
        dict: Статистика по зарплатам в формате:
            {
                'Язык': {
                    'vacancies_found': int,
                    'vacancies_processed': int,
                    'average_salary': int
                }
            }
    """
    town_id = find_hh_town_id(city_name, hh_headers)

    stats = {}
    for lang in languages:
        vacancies, total_found = fetch_hh_vacancies(lang, town_id, hh_headers)
        processed_count, average_salary = calculate_stats(vacancies)
        stats[lang] = {
            'vacancies_found': total_found,  # Используем значение из API
            'vacancies_processed': processed_count,
            'average_salary': average_salary
        }

    return stats
