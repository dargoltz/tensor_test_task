import json
import os

from tensor_test_task.db import batch_insert_hierarchy_items, get_employee_names_by_organization


def import_data_from_json_file(path: str, max_size: int = 10 * 1024 * 1024):
    """
    Добавляет данные об организациях и сотрудниках из JSON файла в БД.

    Args:
        path (str): путь к файлу
        max_size (int): максимальный размер файла в байтах, по умолчанию 10Мб
    """
    if os.path.getsize(path) > max_size:
        raise ValueError

    with open(path, "r") as f:
        data = json.load(f)

    hierarchy_item_values = parse_json(data)

    batch_insert_hierarchy_items(hierarchy_item_values)


def parse_json(data) -> list[tuple[int, int | None, str, str]]:
    """
    Возвращает данные об элементе иерархии в формате для вставки в raw insert запрос

    Args:
        data: list[dict[str, Any]]
    """
    result = []

    for item in data:
        pk = item["id"]
        parent_id = item["ParentId"]
        name = item["Name"]
        hierarchy_item_type = str(item["Type"])  # str тип тк в БД у нас лежит enum

        result.append((pk, parent_id, name, hierarchy_item_type))

    return result

def get_organization_employees(employee_id: int) -> list[str]:
    """
    Возвращает список сотрудников той же организации, что и у указанного сотрудника

    Args:
        employee_id (int): id сотрудника
    """
    employees = get_employee_names_by_organization(employee_id)

    if not employees:  # кейс когда указали не айди сотрудника
        raise ValueError

    return employees