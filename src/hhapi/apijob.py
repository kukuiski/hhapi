from abc import ABC, abstractmethod


class APIJob(ABC):
    """Абстрактный класс для работы с API сайта вакансий"""

    @abstractmethod
    def connect(self) -> None:
        """
        Установить соединение с API.
        Может включать авторизацию или настройку соединения.
        """
        pass

    @abstractmethod
    def search_vacancies(self, keyword: str, count: int = 10) -> list:
        """
        Поиск вакансий по ключевому слову.

        :param keyword: строка для поиска вакансий (например, "Python разработчик")
        :param count: количество вакансий для получения
        :return: список вакансий
        """
        pass

    @abstractmethod
    def get_vacancy_details(self, vacancy_id: str) -> dict:
        """
        Получить подробную информацию о вакансии.

        :param vacancy_id: уникальный идентификатор вакансии
        :return: словарь с подробной информацией о вакансии
        """
        pass
