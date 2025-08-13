import argparse
import requests
from dotenv import load_dotenv
import os
from hh import get_hh_statistics
from sj import get_sj_statistics
from salary_utils import print_stats_table


LANGUAGES = [
    'Python',
    'Java',
    'JavaScript',
    'C#',
    'C++',
    'PHP',
    'Ruby',
    'Go',
    'Swift',
    'Kotlin'
]


def parse_arguments():
    parser = argparse.ArgumentParser(description='Анализ зарплат по языкам программирования')
    parser.add_argument('city', help='Название города для анализа')
    return parser.parse_args()


def main():
    args = parse_arguments()
    city_name = args.city

    load_dotenv()

    # Настройки для HeadHunter
    HH_ACCESS_TOKEN = os.getenv('HH_ACCESS_TOKEN')
    HH_CONTACT_EMAIL = os.getenv('YANDEX_LOGIN')
    
    hh_headers = {
        'Authorization': f'Bearer {HH_ACCESS_TOKEN}',
        'User-Agent': f'MyHHIntegration/1.0 ({HH_CONTACT_EMAIL})'
    }
    
    # Настройки для SuperJob
    SUPER_JOB_SECRET_KEY = os.getenv('SUPER_JOB_SECRET_KEY')
    SUPER_JOB_TOKEN = os.getenv('SUPER_JOB_TOKEN')

    sj_headers = {
        'X-Api-App-Id': SUPER_JOB_SECRET_KEY,
        'Authorization': f'Bearer {SUPER_JOB_TOKEN}',
    }
    
    print('\nСбор статистики с HeadHunter...')
    try:
        hh_stats = get_hh_statistics(city_name, hh_headers, LANGUAGES)
        print_stats_table(hh_stats, city_name, 'HeadHunter')
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f'Ошибка при получении данных HeadHunter: {e}')

    print('\nСбор статистики с SuperJob...')
    try:
        sj_stats = get_sj_statistics(city_name, sj_headers, LANGUAGES)
        print_stats_table(sj_stats, city_name, 'SuperJob')
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f'Ошибка при получении данных SuperJob: {e}')


if __name__ == '__main__':
    main()
