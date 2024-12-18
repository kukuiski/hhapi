from typing import Optional

import requests
from apijob import APIJob


class APIJobHH(APIJob):
    """Класс для сбора вакансий с hh.ru"""

    __VACANCIES_URL = "https://api.hh.ru/vacancies"
    __DICTS_URL = "https://api.hh.ru/dictionaries"
    __HEADERS = {"User-Agent": "HH-User-Agent"}
    __PER_PAGE = 100  # Предопределённое количество результатов поиска на страницу

    __currency_rates = {}  # Атрибут класса для хранения курсов валют

    def __init__(self):
        self.params = {"text": "", "page": 0, "per_page": 100}
        self.__vacancies = []
        self.__detailed_vacancies = []
        if not APIJobHH.__currency_rates:
            APIJobHH.load_currency_rates()

    def connect(self) -> None:
        """
        Отельная установка соединения для hh.ru не требуется
        """
        pass

    def search_vacancies(self, keyword: str, pages_count: int = 1) -> list:
        """
        Метод для поиска вакансий по ключевому слову.
        При каждом новом поиске список найденных вакансий сбрасывается.
        """
        self.params = {"text": keyword, "page": 0, "per_page": APIJobHH.__PER_PAGE}
        self.__vacancies = []
        self.__detailed_vacancies = []

        while self.params.get("page") != pages_count:
            response = requests.get(
                APIJobHH.__VACANCIES_URL, headers=APIJobHH.__HEADERS, params=self.params
            )
            vacancies = response.json().get("items", [])

            # for vacancy in vacancies:
            #     vacancy_details = self.get_vacancy_details(vacancy['id'])
            #     self.__detailed_vacancies.append(vacancy_details)

            self.__vacancies.extend(vacancies)
            self.params["page"] += 1

        return self.__vacancies

    @classmethod
    def get_vacancy_details(cls, vacancy_id: str) -> dict:
        """
        Метод для получения деталей вакансии.
        :param vacancy_id: id вакансии hh.ru
        :return: словарь с данными вакансии
        """
        response = requests.get(
            f"{APIJobHH.__VACANCIES_URL}/{vacancy_id}", headers=APIJobHH.__HEADERS
        )
        if response.status_code != 200:
            raise ConnectionError(f"Ошибка получения данных: {response.status_code}")
        return response.json()

    @classmethod
    def load_currency_rates(cls) -> None:
        """
        Метод для загрузки курсов валют в атрибут класса.
        """
        if not cls.__currency_rates:  # Загружаем курсы только если они ещё не загружены
            response = requests.get(cls.__DICTS_URL, headers=cls.__HEADERS)
            if response.status_code != 200:
                print(f"Ошибка получения данных: {response.status_code}")
                return
            for currency in response.json()["currency"]:
                cls.__currency_rates[currency["code"]] = currency["rate"]

    @classmethod
    def get_currency_rate(cls, currency_code: str) -> Optional[float]:
        """
        Возвращает курс валюты по отношению к рублю
        :return: курс валюты или None, если не найдено
        """
        if not cls.__currency_rates:
            cls.load_currency_rates()
        rate = cls.__currency_rates.get(currency_code, None)
        return rate

    @property
    def currency_rates(self) -> dict:
        """
        Возвращает курсы валют в виде словаря
        """
        self.__class__.load_currency_rates()
        return self.__class__.__currency_rates
