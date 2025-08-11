# Анализ зарплат программистов.

Этот проект собирает статистику по зарплатам разработчиков в выбранном городе для различных языков программирования, используя данные с двух популярных платформ: HeadHunter и SuperJob.

## Основные функции

- Сбор вакансий для 10 популярных языков программирования
- Расчет средней зарплаты с учетом различных схем указания оплаты
- Форматирование результатов в виде таблиц
- Поддержка двух платформ: HeadHunter и SuperJob

## Структура проекта

- hh_sj.py - основной скрипт
- hh_town_id.py - утилита для поиска ID городов в HeadHunter
- sj_town_id.py - утилита для поиска ID городов в SuperJob
- predict_salary.py - модуль расчета зарплат

## Требования

- `Python3`
- Установленные зависимости из `requirements.txt`
- API-ключи для:
    - [HeadHunter](https://api.hh.ru/)
    - [SuperJob](https://api.superjob.ru/)

Чтобы запустить скрипт на `Python`, вам нужен интерпретатор `Python`. `Pip` понадобится, чтобы ставить библиотеки других разработчиков.
Установить `python` по [ссылка на официальный сайт](https://www.python.org/).

## Установка

1. Клонируйте репозиторий

Репозиторий принадлежит не вам, поэтому стоит создать свою собственную копию репозитория. Это называется форком. [Как создать форк (вилку)](https://docs.github.com/ru/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo).

2. Установите зависимости

**Основные зависимости:**
- `python-dotenv = 1.1.0` - необходим для загрузки переменных окружения из `.env` файла
- `requests = 2.32.3` - библиотека для работы с HTTP-запросами в Python, которая упрощает взаимодействие с веб-сервисами и API
- `terminaltables = 3.1.10` - библиотека для построения таблиц

Программа не будет работать без библиотеки `requests`, а она не входит в стандартную библиотеку `Python`. Поставьте её на свой компьютер с помощью [pip](https://dvmn.org/encyclopedia/pip/pip_basic_usage/).

```bash
pip install -r requirements.txt
```

3. Проверьте установку

```bash
python --version  # Должна быть версия Python 3*
pip list          # Должны отобразиться все зависимости, описанные выше
```

## Настройка

**Настройка переменных окружения**

Переменные окружения придётся загружать вручную при каждом запуске терминала. Автоматизируйте процесс с помощью модуля [python-dotenv](https://pypi.org/project/python-dotenv/0.9.1/).

**Переменные:**

### HeadHunter

- HH_CLIENT_ID=your_client_id
- HH_CLIENT_SECRET=your_client_secret
- HH_REDIRECT_URI=your_redirect_uri
- HH_ACCESS_TOKEN=your_access_token
- YANDEX_LOGIN=your_email - контактная почта разработчика

### SuperJob

- SUPER_JOB_SECRET_KEY=your_secret_key
- SUPER_JOB_TOKEN=your_token

1. Создать файл `.env` в корне проекта и добавьте ваши API-ключи:

- HH_CLIENT_ID=your_client_id
- HH_CLIENT_SECRET=your_client_secret
- HH_REDIRECT_URI=your_redirect_uri
- HH_ACCESS_TOKEN=your_access_token
- YANDEX_LOGIN=your_email - контактная почта разработчика
- SUPER_JOB_SECRET_KEY=your_secret_key
- SUPER_JOB_TOKEN=your_token

2. Добавьте `.env` в `.gitignore` чтобы не публиковать конфиденциальные данные.

## Запуск

После настройки и установки зависимостей запустите скрипт.

Открыть терминал и ввести:
```bash
python hh_sj.py --help
```

После запуска вы увидите две таблицы со статистикой по зарплатам для каждого языка программирования в выбранном городе - одну для HeadHunter и одну для SuperJob.

## Пример вывода

<img width="1041" height="776" alt="Снимок экрана 2025-08-07 145529" src="https://github.com/user-attachments/assets/e2b32386-7572-4a7c-9a3d-8ff63d3b967b" />


## Особенности реализации

### Метод расчета зарплат

- Если указана только минимальная зарплата: зарплата = min * 1.2
- Если указана только максимальная зарплата: зарплата = max * 0.8
- Если указаны оба предела: зарплата = (min + max) / 2

### Поддерживаемые языки

Проект анализирует зарплаты для следующих языков программирования:
- Python
- Java
- JavaScript
- C#
- C++
- PHP
- Ruby
- Go
- Swift
- Kotlin

## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
