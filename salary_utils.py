from terminaltables import AsciiTable


def calculate_average_salary(salary_from: float, salary_to: float) -> float:
    """Рассчитывает среднюю зарплату по двум граничным значениям.

    Args:
        salary_from: Нижняя граница зарплаты
        salary_to: Верхняя граница зарплаты

    Returns:
        Рассчитанная средняя зарплата
    """
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    elif salary_from:
        return salary_from * 1.2
    elif salary_to:
        return salary_to * 0.8
    else:
        return None


def process_hh_vacancy(vacancy: dict) -> float:
    """Обрабатывает вакансию HeadHunter.

    Args:
        vacancy: Данные вакансии в формате HH

    Returns:
        Средняя зарплата в рублях или None
    """
    salary_data = vacancy['salary']
    if salary_data['currency'] != 'RUR':
        return None

    return calculate_average_salary(
        salary_data.get('from'),
        salary_data.get('to')
    )


def process_sj_vacancy(vacancy: dict) -> float:
    """Обрабатывает вакансию SuperJob.

    Args:
        vacancy: Данные вакансии в формате SJ

    Returns:
        Средняя зарплата в рублях или None
    """
    if vacancy['currency'] != 'rub':
        return None

    return calculate_average_salary(
        vacancy.get('payment_from'),
        vacancy.get('payment_to')
    )


def predict_rub_salary(vacancy: dict) -> float:
    """Рассчитывает среднюю зарплату в рублях для вакансии.

    Args:
        vacancy: Данные вакансии

    Returns:
        Средняя зарплата в рублях или None
    """
    # Для HeadHunter
    if 'salary' in vacancy and vacancy['salary']:
        return process_hh_vacancy(vacancy)

    # Для SuperJob
    elif all(key in vacancy for key in ['payment_from', 'payment_to']):
        return process_sj_vacancy(vacancy)

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
