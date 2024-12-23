from unittest.mock import patch

import responses
from apijobhh import APIJobHH


@responses.activate
def test_load_currency_rates(mock_currency_rates):
    APIJobHH._APIJobHH__currency_rates = {}  # Очистка перед тестом
    responses.add(
        responses.GET,
        "https://api.hh.ru/dictionaries",
        json={
            "currency": [{"code": "USD", "rate": 75.0}, {"code": "EUR", "rate": 90.0}]
        },
        status=200,
    )

    APIJobHH.load_currency_rates()

    assert APIJobHH._APIJobHH__currency_rates == {"USD": 75.0, "EUR": 90.0}


def test_get_currency_rate(mock_currency_rates):
    with patch.object(APIJobHH, "_APIJobHH__currency_rates", mock_currency_rates):
        assert APIJobHH.get_currency_rate("USD") == 75.0
        assert APIJobHH.get_currency_rate("EUR") == 90.0
        assert APIJobHH.get_currency_rate("GBP") is None


@responses.activate
def test_search_vacancies(mock_vacancies):
    responses.add(
        responses.GET,
        "https://api.hh.ru/vacancies",
        json=mock_vacancies,
        status=200,
    )

    api_job_hh = APIJobHH()
    vacancies = api_job_hh.search_vacancies("developer", pages_count=1)
    assert len(vacancies) == 2
    assert vacancies[0]["name"] == "Python Developer"
    assert vacancies[1]["name"] == "Java Developer"


@responses.activate
def test_get_vacancy_details(mock_vacancy_details):
    responses.add(
        responses.GET,
        "https://api.hh.ru/vacancies/1",
        json=mock_vacancy_details,
        status=200,
    )

    details = APIJobHH.get_vacancy_details("1")
    assert details["id"] == "1"
    assert details["name"] == "Python Developer"
    assert details["description"] == "Development of backend services."


def test_currency_rates_property(mock_currency_rates):
    with patch.object(APIJobHH, "_APIJobHH__currency_rates", mock_currency_rates):
        api_job_hh = APIJobHH()
        assert api_job_hh.currency_rates == mock_currency_rates
