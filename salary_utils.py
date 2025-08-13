from terminaltables import AsciiTable


def predict_rub_salary(vacancy):
    """Рассчитывает среднюю зарплату в рублях для вакансии.
    
    Args:
        vacancy (dict): Данные вакансии

    Returns:
        float or None: Средняя зарплата в рублях или None, если невозможно рассчитать
    """
    # Для HeadHunter
    if 'salary' in vacancy and vacancy['salary']:
        salary_data = vacancy['salary']
        if salary_data['currency'] != 'RUR':
            return None
        salary_from = salary_data['from']
        salary_to = salary_data['to']

    # Для SuperJob
    elif 'payment_from' in vacancy and 'payment_to' in vacancy:
        salary_from = vacancy['payment_from']
        salary_to = vacancy['payment_to']

        # SuperJob: если валюта не рубли, то пропускаем
        if vacancy['currency'] != 'rub':
            return None
    else:
        return None
    
    # Рассчитываем среднюю зарплату
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    elif salary_from:
        return salary_from * 1.2
    elif salary_to:
        return salary_to * 0.8
    else:
        return None


def calculate_stats(vacancies):
    """Вычисляет статистику по вакансиям.
    
    Args:
        vacancies (list): Список вакансий

    Returns:
        tuple: Кортеж из двух элементов:
            - int: Количество обработанных вакансий (с зарплатой)
            - int or None: Средняя зарплата или None, если нет обработанных вакансий
    """
    salaries = []
    for vacancy in vacancies:
        salary = predict_rub_salary(vacancy)
        if salary:
            salaries.append(salary)

    processed_count = len(salaries)

    average_salary = int(sum(salaries) / processed_count) if processed_count else None

    return processed_count, average_salary


def print_stats_table(stats, city_name, source):
    """Форматирует и выводит статистику в виде таблицы в консоль.
    
    Args:
        stats (dict): Статистика в формате:
            {
                'Язык': {
                    'vacancies_found': int,
                    'vacancies_processed': int,
                    'average_salary': int
                }
            }
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
