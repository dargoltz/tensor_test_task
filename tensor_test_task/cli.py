import typer

app = typer.Typer()


@app.command()
def import_data() -> None:
    """
    Добавляет данные об организациях и сотрудниках из JSON файла в БД.
    """
    ...

@app.command()
def get_employees(employee_id: int) -> None:
    """
    Возвращает список сотрудников той же организации, что и у указанного сотрудника

    Args:
        employee_id (int): id сотрудника
    """
    ...