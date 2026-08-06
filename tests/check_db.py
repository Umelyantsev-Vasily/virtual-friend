import psycopg2
import sys

print("1. Пытаемся подключиться...")
try:
    conn = psycopg2.connect(
        user='postgres',
        password='221096',
        database='virtual_friend',
        host='localhost',
        port=5432,
        connect_timeout=5
    )
    print("✅ Подключение успешно!")
    conn.close()
except Exception as e:
    print(f"❌ Ошибка: {e}")
    print(f"Тип ошибки: {type(e)}")