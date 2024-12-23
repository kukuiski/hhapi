import csv
import json
import re
from pathlib import Path

from datajob import DataJob
from vacancyhh import VacancyHH


class DataJobHHJSON(DataJob):
    """
    Класс для управления вакансиями, сохраняемыми в JSON-файл.
    """

    def __init__(
        self,
        file_path: str = "../../data/vacancies.json",
        delete_existing_data: bool = False,
    ):
        """
        Инициализация экземпляра класса для работы с вакансиями в файле.
        :param file_path: Путь к файлу с данными
        :param delete_existing_data: Если передан True, то существующий файл удаляется.
        """

        self.__file_path = Path(file_path)

        if delete_existing_data and self.__file_path.exists():
            self.__file_path.unlink()

    def add(self, vacancy: VacancyHH):
        if not isinstance(vacancy, VacancyHH):
            raise ValueError("Ожидается тип VacancyHH")

        vacancies = self.__load_data()

        # Добавляем или перезаписываем вакансию по ключу ID
        vacancies[vacancy.id] = vacancy.to_dict()
        self.__save_data(vacancies)

    def delete(self, vacancy_id: str):
        vacancies = self.__load_data()
        vacancies.pop(vacancy_id)
        self.__save_data(vacancies)

    def get_vacancies(self, **criteria):
        vacancies = self.__load_data()
        result = []

        for vacancy in vacancies.values():
            if all(
                re.search(value, str(vacancy.get(key, "")), re.IGNORECASE)
                for key, value in criteria.items()
            ):
                result.append(VacancyHH(vacancy))

        return result

    def save_to_csv(self, file_name: str):
        data = self.get_vacancies()
        data_dicts = [
            vacancy.to_dict() for vacancy in data
        ]  # Конвертация объектов в словари
        with open(file_name, mode="w", newline="", encoding="utf-8") as file:
            fieldnames = data_dicts[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data_dicts)

    def __load_data(self):
        try:
            with open(self.__file_path, "r", encoding="utf-8") as f:
                return json.load(f) or {}  # Возвращаем пустой словарь, если файл пуст
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            # Обрабатываем случай пустого или некорректного JSON-файла
            return {}

    def __save_data(self, vacancies):
        with open(self.__file_path, "w", encoding="utf-8") as f:
            json.dump(vacancies, f, ensure_ascii=False, indent=4)
