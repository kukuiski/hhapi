import csv
import json

import pytest
from datajobhhjson import DataJobHHJSON
from vacancyhh import VacancyHH


@pytest.fixture
def temp_json_file(tmp_path):
    """
    Создаёт временный JSON-файл с пустым словарём.
    """
    file_path = tmp_path / "vacancies.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump({}, f)
    return file_path


@pytest.fixture
def mock_vacancy():
    """
    Возвращает объект VacancyHH с тестовыми данными.
    """
    return VacancyHH(
        {
            "id": "1",
            "name": "Python Developer",
            "salary": {"from": 100000, "currency": "RUB"},
        }
    )


@pytest.fixture
def mock_vacancies_data():
    """
    Возвращает словарь с несколькими тестовыми вакансиями.
    """
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


def test_add_vacancy(temp_json_file, mock_vacancy):
    job = DataJobHHJSON(file_path=str(temp_json_file))
    job.add(mock_vacancy)
    with open(temp_json_file, encoding="utf-8") as f:
        data = json.load(f)
    assert mock_vacancy.id in data
    assert data[mock_vacancy.id]["name"] == "Python Developer"


def test_delete_vacancy(temp_json_file, mock_vacancies_data):
    with open(temp_json_file, "w", encoding="utf-8") as f:
        json.dump(mock_vacancies_data, f)
    job = DataJobHHJSON(file_path=str(temp_json_file))
    job.delete("1")
    with open(temp_json_file, encoding="utf-8") as f:
        data = json.load(f)
    assert "1" not in data
    assert "2" in data


def test_get_vacancies(temp_json_file, mock_vacancies_data):
    with open(temp_json_file, "w", encoding="utf-8") as f:
        json.dump(mock_vacancies_data, f)
    job = DataJobHHJSON(file_path=str(temp_json_file))
    result = job.get_vacancies(name="Python")
    assert len(result) == 1
    assert result[0].id == "1"
    assert result[0].name == "Python Developer"


def test_save_to_csv(temp_json_file, mock_vacancies_data, tmp_path):
    with open(temp_json_file, "w", encoding="utf-8") as f:
        json.dump(mock_vacancies_data, f)
    csv_file = tmp_path / "vacancies.csv"
    job = DataJobHHJSON(file_path=str(temp_json_file))
    job.save_to_csv(str(csv_file))
    assert csv_file.exists()
    with open(csv_file, encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
    assert len(reader) == 2
    assert reader[0]["name"] == "Python Developer"
    assert reader[1]["name"] == "Java Developer"


def test_get_vacancies_no_match(temp_json_file, mock_vacancies_data):
    with open(temp_json_file, "w", encoding="utf-8") as f:
        json.dump(mock_vacancies_data, f)
    job = DataJobHHJSON(file_path=str(temp_json_file))
    result = job.get_vacancies(name="C++")
    assert len(result) == 0


def test_add_invalid_type(temp_json_file):
    job = DataJobHHJSON(file_path=str(temp_json_file))
    with pytest.raises(ValueError, match="Ожидается тип VacancyHH"):
        job.add({"id": "3", "name": "Invalid Vacancy"})  # type: ignore


def test_load_data_invalid_json(tmp_path):
    invalid_json_file = tmp_path / "invalid.json"
    with open(invalid_json_file, "w", encoding="utf-8") as f:
        f.write("{invalid_json:}")
    job = DataJobHHJSON(file_path=str(invalid_json_file))
    # Подавляем предупреждение о приватном методе
    data = job._DataJobHHJSON__load_data()  # type: ignore
    assert data == {}
