from apijobhh import APIJobHH
from datajobhhjson import DataJobHHJSON
from vacancyhh import VacancyHH


def main():
    print("Добро пожаловать в систему поиска вакансий!")

    api_job_hh = APIJobHH()
    file_path = input(
        "Введите путь к файлу для сохранения вакансий (по-умолчанию '../../data/vacancies.json'): "
    )
    if not file_path:
        file_path = "../../data/vacancies.json"
    data_job = DataJobHHJSON(file_path, delete_existing_data=False)

    while True:
        print("\nВыберите действие:")
        print("1. Ввести поисковый запрос для запроса вакансий из hh.ru")
        print("2. Получить топ N вакансий по зарплате")
        print("3. Получить вакансии с ключевым словом в названии")
        print("4. Выход")

        choice = input("Введите номер действия: ").strip()

        if choice == "1":
            keyword = input("Введите поисковый запрос: ")
            pages_count = int(input(
                "Введите количество страниц для поиска (по-умолчанию 1): ").strip()
            )
            if not pages_count:
                pages_count = 1

            vacancies = api_job_hh.search_vacancies(keyword, pages_count)
            for vacancy_data in vacancies:
                vacancy = VacancyHH(vacancy_data, api_job_hh.currency_rates)
                data_job.add(vacancy)

            print(f"Найдено и сохранено {len(vacancies)} вакансий.")

        elif choice == "2":
            top_n_input = input("Введите количество вакансий для отображения: ").strip()
            if not top_n_input.isdigit() or int(top_n_input) <= 0:
                print("Ошибка: введите корректное положительное число.")
            else:
                top_n = int(top_n_input)
                vacancies = data_job.get_vacancies()

                sorted_vacancies = sorted(vacancies, reverse=True)

                print("Топ вакансий по зарплате:")
                for vacancy in sorted_vacancies[:top_n]:
                    print(vacancy, "\n")

        elif choice == "3":
            keyword = input("Введите ключевое слово для поиска в названии: ")
            vacancies = data_job.get_vacancies(name=keyword)

            print(f'Найдено {len(vacancies)} вакансий с ключевым словом "{keyword}":')
            for vacancy in vacancies:
                print(vacancy, "\n")

        elif choice == "4":
            print("Выход из программы. До свидания!")
            break

        else:
            print("Ошибка: выберите корректный номер действия.")


if __name__ == "__main__":
    main()
