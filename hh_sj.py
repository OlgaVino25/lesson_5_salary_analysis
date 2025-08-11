import argparse
import requests
from dotenv import load_dotenv
import os
from hh_town_id import find_hh_town_id
from sj_town_id import find_town_id
from predict_salary import predict_rub_salary
from terminaltables import AsciiTable


LANGUAGES = {
    'Python': 'Python',
    'Java': 'Java',
    'JavaScript': 'JavaScript',
    'C#': 'C#',
    'C++': 'C++',
    'PHP': 'PHP',
    'Ruby': 'Ruby',
    'Go': 'Go',
    'Swift': 'Swift',
    'Kotlin': 'Kotlin'
}


def fetch_hh_vacancies(language_query, area_id, hh_headers):
    """Получает все вакансии по языку программирования и городу с HeadHunter API.

    Args:
        language_query (str): Название языка программирования для поиска
        area_id (int): ID города в API HeadHunter

    Returns:
        list: Список вакансий (словарей)
    """
    all_vacancies = []
    page = 0
    max_attempts = 3  # Максимальное количество попыток для одной страницы

    try:
        initial_response = requests.get(
            'https://api.hh.ru/vacancies',
            headers=hh_headers,
            params={
                'text': language_query,
                'area': area_id,
                'per_page': 100,
                'page': 0
            }
        )
        initial_response.raise_for_status()
        initial_hh_vacancy = initial_response.json()
        total_pages = initial_hh_vacancy.get('pages', 0)
        all_vacancies.extend(initial_hh_vacancy.get('items', []))
        page = 1
    except requests.exceptions.RequestException as e:
        print(f'Ошибка при загрузке первой страницы: {e}')
        total_pages = 0

    while page < total_pages:
        attempts = 0
        success = False
        
        while attempts < max_attempts and not success:
            try:
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
                hh_vacancy = response.json()
                vacancies = hh_vacancy.get('items', [])
                all_vacancies.extend(vacancies)
                success = True
                
            except requests.exceptions.RequestException as e:
                attempts += 1
                if attempts < max_attempts:
                    print(f'Повторная попытка ({attempts}/{max_attempts}) для страницы {page}...')
                else:
                    print(f'Ошибка при загрузке страницы {page} после {max_attempts} попыток: {e}')
        
        page += 1

    return all_vacancies


def fetch_sj_vacancies(language_query, town_id, sj_headers):
    """Получает все вакансии по языку программирования и городу с SuperJob API.

    Args:
        language_query (str): Название языка программирования для поиска
        town_id (int): ID города в API SuperJob

    Returns:
        list: Список вакансий (словарей)
    """
    all_vacancies = []
    page = 0
    max_attempts = 3  # Максимальное количество попыток для одной страницы
    has_more = True
    
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
                    timeout=10  # Таймаут для запроса
                )
                response.raise_for_status()
                sj_vacancy = response.json()
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

    return all_vacancies


def calculate_hh_stats(vacancies):
    """Вычисляет статистику по вакансиям HeadHunter.

    Args:
        vacancies (list): Список вакансий от API HH

    Returns:
        dict: Словарь со статистикой:
        {
            'vacancies_found': общее количество вакансий,
            'vacancies_processed': количество обработанных зарплат,
            'average_salary': средняя зарплата в рублях
        }
    """
    salaries = []
    for vacancy in vacancies:
        salary = predict_rub_salary(vacancy)
        if salary:
            salaries.append(salary)

    processed_count = len(salaries)
    average_salary = int(sum(salaries) / processed_count) if salaries else None

    return {
        'vacancies_found': len(vacancies),
        'vacancies_processed': processed_count,
        'average_salary': average_salary
    }


def calculate_sj_stats(vacancies):
    """Вычисляет статистику по вакансиям SuperJob.

    Args:
        vacancies (list): Список вакансий от API SJ

    Returns:
        dict: Словарь со статистикой:
        {
            'vacancies_found': общее количество вакансий,
            'vacancies_processed': количество обработанных зарплат,
            'average_salary': средняя зарплата в рублях
        }
    """
    salaries = []
    for vacancy in vacancies:
        salary = predict_rub_salary(vacancy)
        if salary:
            salaries.append(salary)

    processed_count = len(salaries)
    average_salary = int(sum(salaries) / processed_count) if salaries else None

    return {
        'vacancies_found': len(vacancies),
        'vacancies_processed': processed_count,
        'average_salary': average_salary
    }


def get_hh_statistics(city_name, hh_headers):
    """Получает статистику по всем языкам программирования для города с HeadHunter.

    Args:
        city_name (str): Название города для поиска

    Returns:
        dict/None: Словарь вида {язык: статистика} или None если город не найден
    """
    try:
        town_id = find_hh_town_id(city_name, hh_headers)

        stats = {}
        for lang, query in LANGUAGES.items():
            vacancies = fetch_hh_vacancies(query, town_id, hh_headers)
            lang_stats = calculate_hh_stats(vacancies)
            stats[lang] = lang_stats

        return stats
        
    except requests.exceptions.RequestException as e:
        print(f'Ошибка при запросе к HeadHunter: {e}')
        return None
    except ValueError as e:
        print(e)
        return None


def get_sj_statistics(city_name, sj_headers):
    """Получает статистику по всем языкам программирования для города с SuperJob.

    Args:
        city_name (str): Название города для поиска

    Returns:
        dict/None: Словарь вида {язык: статистика} или None если город не найден
    """
    try:
        town_id = find_town_id(city_name, sj_headers)

        stats = {}
        for lang, query in LANGUAGES.items():
            vacancies = fetch_sj_vacancies(query, town_id, sj_headers)
            lang_stats = calculate_sj_stats(vacancies)
            stats[lang] = lang_stats

        return stats
        
    except requests.exceptions.RequestException as e:
        print(f'Ошибка при запросе к SuperJob: {e}')
        return None
    except ValueError as e:
        print(e)
        return None


def print_stats_table(stats, city_name, source):
    """Форматирует и выводит статистику в виде таблицы в консоль.

    Args:
        stats (dict): Статистика по языкам программирования
        city_name (str): Название города для отображения
        source (str): Источник данных ('HeadHunter'/'SuperJob')
    """
    table_data = [
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
    ]

    for lang, stat in stats.items():
        table_data.append([
            lang.lower(),
            stat['vacancies_found'],
            stat['vacancies_processed'],
            stat['average_salary'] or 'N/A'
        ])

    title = f'{source} {city_name}'
    table = AsciiTable(table_data, title)
    print(table.table)


def main(city_name):
    load_dotenv()

    # Настройки для HeadHunter
    HH_ACCESS_TOKEN = os.getenv('HH_ACCESS_TOKEN')
    YANDEX_LOGIN = os.getenv('YANDEX_LOGIN')
    
    hh_headers = {
        'Authorization': f'Bearer {HH_ACCESS_TOKEN}',
        'User-Agent': f'MyHHIntegration/1.0 ({YANDEX_LOGIN})'
    }
    
    # Настройки для SuperJob
    SUPER_JOB_SECRET_KEY = os.getenv('SUPER_JOB_SECRET_KEY')
    SUPER_JOB_TOKEN = os.getenv('SUPER_JOB_TOKEN')

    sj_headers = {
        'X-Api-App-Id': SUPER_JOB_SECRET_KEY,
        'Authorization': f'Bearer {SUPER_JOB_TOKEN}',
    }
    
    print('\nСбор статистики с HeadHunter...')
    hh_stats = get_hh_statistics(city_name, hh_headers)
    if hh_stats:
        print_stats_table(hh_stats, city_name, 'HeadHunter')

    print('\nСбор статистики с SuperJob...')
    sj_stats = get_sj_statistics(city_name, sj_headers)
    if sj_stats:
        print_stats_table(sj_stats, city_name, 'SuperJob')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Анализ зарплат по языкам программирования')
    parser.add_argument('city', help='Название города для анализа')
    args = parser.parse_args()
    main(args.city)
