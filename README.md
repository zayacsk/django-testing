# Django Testing

Учебный проект по тестированию веб-приложений на Django в рамках курса Яндекс Практикума.

В репозитории собраны два проекта — **YaNews** и **YaNote**. Для проверки их функциональности используются автоматические тесты.

## Технологии

- Python 3.10
- Django 5.1.1
- pytest
- pytest-django
- unittest
- flake8

## Проекты

### YaNews

Приложение для публикации и обсуждения новостей.

Тесты находятся в директории `ya_news/news/pytest_tests/`.

### YaNote

Приложение для создания и управления личными заметками.

Тесты находятся в директории `ya_note/notes/tests/`.

## Запуск проекта

### 1. Клонирование репозитория

```bash
git clone https://github.com/zayacsk/django-testing.git
cd django-testing
```

### 2. Создание виртуального окружения

Linux / macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Установка зависимостей

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Запуск проверок

Из корневой директории проекта выполните:

```bash
bash run_tests.sh
```

Скрипт последовательно проверяет стиль кода с помощью `flake8`, структуру проекта и тесты обоих приложений.

## Структура проекта

```text
django-testing/
├── ya_news/
│   └── news/
│       └── pytest_tests/  # Тесты YaNews
├── ya_note/
│   └── notes/
│       └── tests/         # Тесты YaNote
├── requirements.txt
├── run_tests.sh
├── setup.cfg
├── structure_test.py
└── README.md
```

## Автор

**Денис Анохин**

GitHub: [@zayacsk](https://github.com/zayacsk)
