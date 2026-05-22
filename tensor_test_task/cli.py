import os
import json

import typer
from psycopg.errors import UniqueViolation, DatabaseError
from .service import import_data_from_json_file, get_organization_employees

app = typer.Typer()


@app.command()
def import_data() -> None:
    """
    Добавляет данные об организациях и сотрудниках из JSON файла в БД.
    """
    try:
        path = os.getenv("DEFAULT_DATA_PATH")

        if not path:
            typer.echo("Не указан путь к файлу с данными для импорта")
            return

        import_data_from_json_file(path)

        typer.echo("Импорт завершен")
    except (KeyError, TypeError, json.JSONDecodeError):
        typer.echo("JSON файл составлен некорректно")
    except FileNotFoundError:
        typer.echo("Файл для импорта отсутствует или адрес указан некорректно")
    except PermissionError:
        typer.echo("Нет прав на чтение файла или проверку размера")
    except UniqueViolation:
        typer.echo("Данные из JSON файла уже импортированы")
    except DatabaseError:
        typer.echo("Ошибка при выполнении запроса")
    except ValueError:
        typer.echo("Файл слишком большой. Максимальный размер - 10Мб")


@app.command()
def get_employees(employee_id: int) -> None:
    """
    Возвращает список сотрудников той же организации, что и у указанного сотрудника

    Args:
        employee_id (int): id сотрудника
    """
    try:
        employees = get_organization_employees(employee_id)

        typer.echo("Cписок сотрудников:")
        for employee in employees:
            typer.echo(employee)
    except ValueError:
        typer.echo("Необходимо указать ID сотрудника")
    except DatabaseError:
        typer.echo("Ошибка при выполнении запроса")
