import requests
from dotenv import load_dotenv
import os
from hh_town_id import find_hh_town_id
from sj_town_id import find_town_id
from terminaltables import AsciiTable

load_dotenv()

# Настройки для HeadHunter
HH_CLIENT_ID = os.getenv('HH_CLIENT_ID')
HH_CLIENT_SECRET = os.getenv('HH_CLIENT_SECRET')
HH_REDIRECT_URI = os.getenv('HH_REDIRECT_URI')
HH_ACCESS_TOKEN = os.getenv('HH_ACCESS_TOKEN')
YANDEX_LOGIN = os.getenv('YANDEX_LOGIN')

HH_HEADERS = {
    'Authorization': f'Bearer {HH_ACCESS_TOKEN}',
    'User-Agent': 'MyHHIntegration/1.0 ({YANDEX_LOGIN})'
}

# Настройки для SuperJob
SUPER_JOB_SECRET_KEY = os.getenv('SUPER_JOB_SECRET_KEY')
SUPER_JOB_TOKEN = os.getenv('SUPER_JOB_TOKEN')

SJ_HEADERS = {
    'X-Api-App-Id': SUPER_JOB_SECRET_KEY,
    'Authorization': f'Bearer {SUPER_JOB_TOKEN}',
}

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


def predict_rub_salary_hh(vacancy):
    """Рассчитывает среднюю зарплату в рублях для вакансии HeadHunter.

    Args:
        vacancy (dict): Словарь с данными вакансии от API HH

    Returns:
        float/None: Средняя зарплата или None если:
        - Зарплата не указана
        - Валюта не рубли
        - Недостаточно данных для расчета
    """
    salary = vacancy.get('salary')
    if not salary or salary.get('currency') != 'RUR':
        return None

    salary_from = salary.get('from')
    salary_to = salary.get('to')

    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    elif salary_from:
        return salary_from * 1.2
    elif salary_to:
        return salary_to * 0.8
    return None


def predict_rub_salary_sj(vacancy):
    """Рассчитывает среднюю зарплату в рублях для вакансии SuperJob.

    Args:
        vacancy (dict): Словарь с данными вакансии от API SJ

    Returns:
        float/None: Средняя зарплата или None если:
        - Зарплата не указана
        - Валюта не рубли
        - Недостаточно данных для расчета
    """
    payment_from = vacancy.get('payment_from')
    payment_to = vacancy.get('payment_to')
    currency = vacancy.get('currency')

    if not currency or currency != 'rub':
        return None

    if payment_from and payment_to:
        return (payment_from + payment_to) / 2
    elif payment_from:
        return payment_from * 1.2
    elif payment_to:
        return payment_to * 0.8
    return None


def fetch_hh_vacancies(language_query, area_id):
    """Получает все вакансии по языку программирования и городу с HeadHunter API.

    Args:
        language_query (str): Название языка программирования для поиска
        area_id (int): ID города в API HeadHunter

    Returns:
        list: Список вакансий (словарей)
    """
    all_vacancies = []
    page = 0
    while True:
        try:
            response = requests.get(
                'https://api.hh.ru/vacancies',
                headers=HH_HEADERS,
                params={
                    'text': language_query,
                    'area': area_id,
                    'per_page': 100,
                    'page': page
                }
            )
            response.raise_for_status()
            data = response.json()

            vacancies = data.get('items', [])
            all_vacancies.extend(vacancies)

            if page >= data.get('pages', 1) - 1:
                break
            page += 1

        except requests.exceptions.RequestException as e:
            print(f'Ошибка при загрузке страницы {page}: {e}')
            break

    return all_vacancies


def fetch_sj_vacancies(language_query, town_id):
    """Получает все вакансии по языку программирования и городу с SuperJob API.

    Args:
        language_query (str): Название языка программирования для поиска
        town_id (int): ID города в API SuperJob

    Returns:
        list: Список вакансий (словарей)
    """
    all_vacancies = []
    page = 0

    while True:
        try:
            response = requests.get(
                'https://api.superjob.ru/2.0/vacancies/',
                headers=SJ_HEADERS,
                params={
                    'keyword': language_query,
                    'town': town_id,
                    'count': 100,
                    'page': page
                }
            )
            response.raise_for_status()
            data = response.json()

            vacancies = data.get('objects', [])
            all_vacancies.extend(vacancies)

            if not data.get('more', False):
                break
            page += 1

        except requests.exceptions.RequestException as e:
            print(f'Ошибка при загрузке страницы {page}: {e}')
            break

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
        salary = predict_rub_salary_hh(vacancy)
        if salary is not None:
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
        salary = predict_rub_salary_sj(vacancy)
        if salary is not None:
            salaries.append(salary)

    processed_count = len(salaries)
    average_salary = int(sum(salaries) / processed_count) if salaries else None

    return {
        'vacancies_found': len(vacancies),
        'vacancies_processed': processed_count,
        'average_salary': average_salary
    }


def get_hh_statistics(city_name):
    """Получает статистику по всем языкам программирования для города с HeadHunter.

    Args:
        city_name (str): Название города для поиска

    Returns:
        dict/None: Словарь вида {язык: статистика} или None если город не найден
    """
    town_id = find_hh_town_id(city_name)
    if not town_id:
        print(f"Город '{city_name}' не найден в HeadHunter")
        return None

    stats = {}
    for lang, query in LANGUAGES.items():
        vacancies = fetch_hh_vacancies(query, town_id)
        lang_stats = calculate_hh_stats(vacancies)
        stats[lang] = lang_stats

    return stats


def get_sj_statistics(city_name):
    """Получает статистику по всем языкам программирования для города с SuperJob.

    Args:
        city_name (str): Название города для поиска

    Returns:
        dict/None: Словарь вида {язык: статистика} или None если город не найден
    """
    town_id = find_town_id(city_name)
    if not town_id:
        print(f"Город '{city_name}' не найден в SuperJob")
        return None

    stats = {}
    for lang, query in LANGUAGES.items():
        vacancies = fetch_sj_vacancies(query, town_id)
        lang_stats = calculate_sj_stats(vacancies)
        stats[lang] = lang_stats

    return stats


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


def main():
    city_name = input('Введите город: ')

    print('\nСбор статистики с HeadHunter...')
    hh_stats = get_hh_statistics(city_name)
    if hh_stats:
        print_stats_table(hh_stats, city_name, 'HeadHunter')

    print('\nСбор статистики с SuperJob...')
    sj_stats = get_sj_statistics(city_name)
    if sj_stats:
        print_stats_table(sj_stats, city_name, 'SuperJob')


if __name__ == '__main__':
    main()
