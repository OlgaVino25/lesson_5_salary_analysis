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
    hh_access_token = os.getenv('HH_ACCESS_TOKEN')
    hh_contact_email = os.getenv('HH_CONTACT_EMAIL')

    hh_headers = {
        'Authorization': f'Bearer {hh_access_token}',
        'User-Agent': f'MyHHIntegration/1.0 ({hh_contact_email})'
    }

    # Настройки для SuperJob
    super_job_secret_key = os.getenv('SUPER_JOB_SECRET_KEY')
    super_job_token = os.getenv('SUPER_JOB_TOKEN')

    sj_headers = {
        'X-Api-App-Id': super_job_secret_key,
        'Authorization': f'Bearer {super_job_token}',
    }

    print('\nСбор статистики с HeadHunter...')
    try:
        hh_stats = get_hh_statistics(city_name, hh_headers, LANGUAGES)
        print_stats_table(hh_stats, city_name, 'HeadHunter')
    except requests.exceptions.RequestException as e:
        print(f'Сетевая ошибка при подключении к HeadHunter: {e}')
    except ValueError as e:
        print(f'Ошибка данных HeadHunter: {e}')

    print('\nСбор статистики с SuperJob...')
    try:
        sj_stats = get_sj_statistics(city_name, sj_headers, LANGUAGES)
        print_stats_table(sj_stats, city_name, 'SuperJob')
    except requests.exceptions.RequestException as e:
        print(f'Сетевая ошибка при подключении к SuperJob: {e}')
    except ValueError as e:
        print(f'Ошибка данных SuperJob: {e}')


if __name__ == '__main__':
    main()
