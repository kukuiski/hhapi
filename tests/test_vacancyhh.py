import pytest
from vacancyhh import VacancyHH


def test_vacancy_initialization():
    vacancy_data = {
        "id": "1",
        "url": "http://example.com",
        "name": "Python Developer",
        "published_at": "2024-01-01",
        "employer": {"name": "Company XYZ"},
        "salary": {"from": 100000, "to": 150000, "currency": "USD"},
    }
    currency_rates = {"USD": 75.0}

    vacancy = VacancyHH(vacancy_data, currency_rates)
    assert vacancy.id == "1"
    assert vacancy.url == "http://example.com"
    assert vacancy.name == "Python Developer"
    assert vacancy.published_at == "2024-01-01"
    assert vacancy.employer == "Company XYZ"
    assert vacancy.salary == 2000  # 150000 / 75


def test_vacancy_without_salary():
    vacancy_data = {"id": "2", "name": "Java Developer"}
    vacancy = VacancyHH(vacancy_data)
    assert vacancy.salary is None
    assert vacancy.employer is None


def test_invalid_vacancy_data():
    with pytest.raises(ValueError, match="Ожидается словарь с данными вакансии."):
        VacancyHH("not a dict")

    with pytest.raises(ValueError, match="Ожидается наличие id вакансии."):
        VacancyHH({})


def test_to_dict():
    vacancy_data = {
        "id": "3",
        "url": "http://example.com",
        "name": "C++ Developer",
        "salary": {"from": 50000, "to": 70000},
    }
    vacancy = VacancyHH(vacancy_data)
    result = vacancy.to_dict()
    assert result == {
        "id": "3",
        "url": "http://example.com",
        "name": "C++ Developer",
        "employer": None,
        "published_at": None,
        "salary": 70000,
    }


def test_vacancy_comparisons():
    v1 = VacancyHH({"id": "1", "salary": {"from": 100000}})
    v2 = VacancyHH({"id": "2", "salary": {"from": 120000}})
    v3 = VacancyHH({"id": "3", "salary": None})

    assert v1 < v2
    assert v2 > v1
    assert v1 == 100000
    assert v3 < 1000
    assert v3 != v1


def test_vacancy_string_representation():
    vacancy_data = {
        "id": "4",
        "name": "Frontend Developer",
        "salary": {"from": 90000},
    }
    vacancy = VacancyHH(vacancy_data)
    expected_str = (
        "ID: 4\n"
        "Вакансия: Frontend Developer\n"
        "Работодатель: None\n"
        "URL: None\n"
        "Дата публикации: None\n"
        "Зарплата: 90 000 ₽"
    )
    assert str(vacancy) == expected_str
