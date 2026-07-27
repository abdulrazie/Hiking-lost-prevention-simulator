from database import get_connection

connection = get_connection()

rows = connection.execute("""
    SELECT id, name, role, status
    FROM people
    ORDER BY id
""").fetchall()

for row in rows:
    print(dict(row))

connection.close()