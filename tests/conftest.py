import json

import pytest
from vacancyhh import VacancyHH


@pytest.fixture
def mock_currency_rates():
    return {
        "USD": 75.0,
        "EUR": 90.0,
    }


@pytest.fixture
def mock_vacancies():
    return {
        "items": [
            {"id": "1", "name": "Python Developer", "salary": None},
            {"id": "2", "name": "Java Developer", "salary": None},
        ]
    }


@pytest.fixture
def mock_vacancy_details():
    return {
        "id": "1",
        "name": "Python Developer",
        "description": "Development of backend services.",
    }


@pytest.fixture
def temp_json_file(tmp_path):
    file_path = tmp_path / "vacancies.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump({}, f)
    return file_path


@pytest.fixture
def mock_vacancy():
    return VacancyHH(
        {
            "id": "1",
            "name": "Python Developer",
            "salary": {"from": 100000, "currency": "RUB"},
            "url": "http://example.com",
        }
    )


@pytest.fixture
def mock_vacancies_data():
    return {
        "1": {
            "id": "1",
            "name": "Python Developer",
            "salary": 100000,
            "url": "http://example.com",
        },
        "2": {
            "id": "2",
            "name": "Java Developer",
            "salary": 120000,
            "url": "http://example.com",
        },
    }
