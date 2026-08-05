import psycopg2
from app.config import settings

try:
    conn = psycopg2.connect(settings.DATABASE_URL)
    print('✅ Подключение к PostgreSQL успешно!')
    conn.close()
except Exception as e:
    print(f'❌ Ошибка: {e}')