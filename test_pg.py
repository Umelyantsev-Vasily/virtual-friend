import psycopg2
import locale

# Принудительно устанавливаем английскую локаль
locale.setlocale(locale.LC_ALL, 'C')

try:
    conn = psycopg2.connect(
        user='friend',
        password='friend123',
        database='virtual_friend',
        host='localhost',
        port=5432
    )
    print('SUCCESS: PostgreSQL connected!')
    conn.close()
except Exception as e:
    print(f'ERROR: {str(e).encode("ascii", errors="replace").decode()}')