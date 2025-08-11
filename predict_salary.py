def predict_rub_salary(vacancy):
    """Рассчитывает среднюю зарплату в рублях для вакансии.

    Args:
        vacancy (dict): Словарь с данными вакансии

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