import os

from psycopg import connect


def batch_insert_hierarchy_items(
    values: list[tuple[int, int | None, str, str]],
) -> None:
    """
    Выполняет массовую вставку записей в таблицу hierarchy_items.

    Args:
        values: [(id, parent_id, name, type), ...]
    """
    if not values:
        return

    query = """
        INSERT INTO hierarchy_items (id, parent_id, name, type)
        VALUES (%s, %s, %s, %s)
    """

    with connect(os.getenv("DB_URL")) as connection:
        with connection.cursor() as cur:
            cur.executemany(query, values)

        connection.commit()


def get_employee_names_by_organization(employee_id: int) -> list[str]:
    """
    Возвращает массив строк с сотрудниками той же организации, что и у переданного сотрудника

    Args:
        employee_id (int): id сотрудника
    """
    query = f"""
        WITH RECURSIVE upward AS (
            -- стартуем с сотрудника
            SELECT id, parent_id, type
            FROM hierarchy_items
            WHERE id = %s AND type = '3'

            UNION ALL

            -- поднимаемся вверх по родителям
            SELECT h.id, h.parent_id, h.type
            FROM hierarchy_items h JOIN upward u ON u.parent_id = h.id
        ),

        org AS (
            -- находим организацию сотрудника
            SELECT id
            FROM upward
            WHERE type = '1'
        ),

        employees_in_org AS (
            -- обходим всё дерево организации вниз
            SELECT h.id, h.parent_id, h.name, h.type
            FROM hierarchy_items h JOIN org o ON h.id = o.id

            UNION ALL

            SELECT h.id, h.parent_id, h.name, h.type
            FROM hierarchy_items h JOIN employees_in_org eio ON h.parent_id = eio.id
        )

        -- выбираем только имена сотрудников
        SELECT name
        FROM employees_in_org
        WHERE type = '3';
    """

    with connect(os.getenv("DB_URL")) as connection:
        with connection.cursor() as cur:
            cur.execute(query, (employee_id,))
            rows = cur.fetchall()

    return [row[0] for row in rows]
