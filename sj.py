import requests
from salary_utils import calculate_stats


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


def fetch_sj_vacancies(language_query, town_id, sj_headers):
    """Получает все вакансии по языку программирования и городу с SuperJob API.

    Args:
        language_query (str): Язык программирования для поиска
        town_id (int): ID города в API SuperJob
        sj_headers (dict): Заголовки для запроса к API SuperJob

    Returns:
        tuple: Кортеж из двух элементов:
            - list: Список вакансий
            - int: Общее количество найденных вакансий (из API)
    """
    all_vacancies = []
    page = 0
    max_attempts = 3
    has_more = True
    total_found = 0

    while has_more:
        attempts = 0
        success = False
        current_page = page

        while attempts < max_attempts and not success:
            try:
                response = requests.get(
                    'https://api.superjob.ru/2.0/vacancies/',
                    headers=sj_headers,
                    params={
                        'keyword': language_query,
                        'town': town_id,
                        'count': 100,
                        'page': current_page
                    },
                    timeout=10
                )
                response.raise_for_status()
                sj_vacancy = response.json()
                if page == 0:
                    total_found = sj_vacancy.get('total', 0)

                vacancies = sj_vacancy.get('objects', [])
                all_vacancies.extend(vacancies)
                has_more = sj_vacancy.get('more', False)
                success = True

            except requests.exceptions.RequestException as e:
                attempts += 1
                if attempts < max_attempts:
                    print(f'Повторная попытка ({attempts}/{max_attempts}) для страницы {current_page}...')
                else:
                    print(f'Ошибка при загрузке страницы {current_page} после {max_attempts} попыток: {e}')
                    has_more = False

        page += 1

    return all_vacancies, total_found


def get_sj_statistics(city_name, sj_headers, languages):
    """Получает статистику по всем языкам программирования для города с SuperJob.

    Args:
        city_name (str): Название города для поиска
        sj_headers (dict): Заголовки для запроса к API SuperJob
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
    town_id = find_town_id(city_name, sj_headers)

    stats = {}
    for lang in languages:
        vacancies, total_found = fetch_sj_vacancies(lang, town_id, sj_headers)
        processed_count, average_salary = calculate_stats(vacancies)
        stats[lang] = {
            'vacancies_found': total_found,
            'vacancies_processed': processed_count,
            'average_salary': average_salary
        }

    return stats
