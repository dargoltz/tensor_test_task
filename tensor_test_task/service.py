import json
import os



def import_data_from_json_file(path: str, max_size: int = 10 * 1024 * 1024):
    """
    Добавляет данные об организациях и сотрудниках из JSON файла в БД.

    Args:
        path (str): путь к файлу
        max_size (int): максимальный размер файла в байтах, по умолчанию 10Мб
    """
    # open file
    # parse json
    # batch insert
    ...


def parse_json(data) -> list[tuple[int, int | None, str, str]]:
    """
    Возвращает данные об элементе иерархии в формате для вставки в raw insert запрос

    Args:
        data: list[dict[str, Any]]
    """
    ...

def get_organization_employees(employee_id: int) -> list[str]:
    """
    Возвращает список сотрудников той же организации, что и у указанного сотрудника

    Args:
        employee_id (int): id сотрудника
    """
    ...