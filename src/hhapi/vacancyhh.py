from functools import total_ordering


@total_ordering
class VacancyHH:
    """
    Класс для работы с вакансиями hh.ru
    При инициализации на вход должен подаваться словарь с данными из hh.ru
    """

    __slots__ = (
        "id",
        "url",
        "name",
        "published_at",
        "description",
        "employer",
        "salary",
    )

    def __init__(self, vacancy: dict, currency_rates_from_hh: dict = None):

        if not isinstance(vacancy, dict):
            raise ValueError("Ожидается словарь с данными вакансии.")

        self.id = vacancy.get("id")
        if not self.id:
            raise ValueError("Ожидается наличие id вакансии.")

        self.url = vacancy.get("url")
        self.name = vacancy.get("name")
        self.published_at = vacancy.get("published_at")
        # self.description = vacancy.get("description")
        self.employer = self.__prepare_employer(vacancy)
        self.salary = self.__prepare_salary(vacancy, currency_rates_from_hh)

    @staticmethod
    def __prepare_employer(vacancy: dict):
        """
        Проверяем, являются ли переданные данные в словаре нашим внутренним форматом.
        Если нет, то обрабатываем как данные в формате hh.ru
        """
        employer = vacancy.get("employer")
        if isinstance(employer, dict):
            employer = employer.get("name")
        return employer

    @staticmethod
    def __prepare_salary(vacancy: dict, currency_rates_from_hh: dict = None):
        """
        Проверяем, являются ли переданные данные в словаре нашим внутренним форматом.
        Если не являются, то обрабатываем как данные в формате hh.ru
        Забираем границы зарплаты "от" и "до" в рублях.
        В случае, если исходные данные хранятся в валюте, отличной от рублей,
        значения конвертируются в рубли на основании текущего курса hh.ru
        Если неожиданно окажется, что переданный код валюты отсутствует в справочнике,
        выбрасывается ошибка из-за высокой вероятности ошибки в данных.
        """
        salary_data = vacancy.get("salary")

        # Если salary_data float или int, значит на вход был подан тип данных словаря VacancyHH
        if isinstance(salary_data, (int, float)):
            return salary_data

        # Если salary_data не словарь или он пустой, то сразу возвращаем None
        if not isinstance(salary_data, dict) or not salary_data:
            return None

        # Считаем, что на входе данные из hh.ru и вычисляем salary —
        # получаем максимальную зарплату из указанных границ "от" и "до" или None.
        salary_from = salary_data.get("from") or 0
        salary_to = salary_data.get("to") or 0
        currency_code = salary_data.get("currency")

        if currency_code and currency_rates_from_hh:
            rate = currency_rates_from_hh.get(currency_code)
            if rate:
                salary_from /= rate
                salary_to /= rate

        result = max(salary_from, salary_to)
        return result if result > 0 else None

    def to_dict(self):
        return {
            "id": self.id,
            "url": self.url,
            "name": self.name,
            "employer": self.employer,
            "published_at": self.published_at,
            "salary": self.salary,
        }

    def __str__(self):
        """
        Возвращает строковое представление объекта VacancyHH.
        """
        salary_str = (
            f"{self.salary:,.0f} ₽".replace(",", " ")
            if self.salary is not None
            else "Не указана"
        )
        return (
            f"ID: {self.id}\n"
            f"Вакансия: {self.name}\n"
            f"Работодатель: {self.employer}\n"
            f"URL: {self.url}\n"
            f"Дата публикации: {self.published_at}\n"
            f"Зарплата: {salary_str}"
        )

    def __eq__(self, other):
        """
        Сравнивает зарплаты двух объектов VacancyHH или объекта VacancyHH с числом.
        Если зарплата отсутствует (None), считается, что объекты не равны.
        """
        if isinstance(other, VacancyHH):
            if self.salary is None or other.salary is None:
                return False
            return self.salary == other.salary
        elif isinstance(other, (float, int)):
            if self.salary is None:
                return False
            return self.salary == other
        return NotImplemented

    def __lt__(self, other):
        """
        Сравнивает зарплаты двух объектов VacancyHH или объекта VacancyHH с числом.
        Вакансии с зарплатой None считаются минимальными.
        """
        if isinstance(other, VacancyHH):
            if self.salary is None:
                return other.salary is not None
            if other.salary is None:
                return False
            return self.salary < other.salary
        elif isinstance(other, (float, int)):
            if self.salary is None:
                return True
            return self.salary < other
        return NotImplemented
