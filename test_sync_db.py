import psycopg2

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
    print(f'ERROR: {e}')
