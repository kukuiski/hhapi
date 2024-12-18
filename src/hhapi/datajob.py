from abc import ABC, abstractmethod


class DataJob(ABC):
    """
    Абстрактный класс для управления вакансиями.
    """

    @abstractmethod
    def add(self, vacancy):
        """
        Метод для добавления вакансии в файл.
        """
        pass

    @abstractmethod
    def delete(self, vacancy_id: str):
        """
        Метод для удаления информации о вакансии по её ID.
        """
        pass

    @abstractmethod
    def get_vacancies(self, **criteria):
        """
        Метод для получения данных о вакансиях из файла по указанным критериям.
        """
        pass
