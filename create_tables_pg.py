import psycopg2
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, JSON, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Character(Base):
    __tablename__ = 'characters'
    id = Column(Integer, primary_key=True)
    user_telegram_id = Column(String(100), nullable=False)
    name = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(20))
    personality = Column(Text, nullable=False)
    traits = Column(JSON)
    response_speed = Column(String(30))
    backstory = Column(Text)
    role = Column(String(30))
    current_mood = Column(String(30))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, nullable=False)
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

try:
    # Подключаемся напрямую к PostgreSQL
    conn = psycopg2.connect(
        user='friend',
        password='friend123',
        database='virtual_friend',
        host='localhost',
        port=5432
    )
    conn.autocommit = True
    cursor = conn.cursor()

    # Создаём таблицы
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS characters (
            id SERIAL PRIMARY KEY,
            user_telegram_id VARCHAR(100) NOT NULL,
            name VARCHAR(50) NOT NULL,
            age INTEGER NOT NULL,
            gender VARCHAR(20),
            personality TEXT NOT NULL,
            traits JSON,
            response_speed VARCHAR(30),
            backstory TEXT,
            role VARCHAR(30),
            current_mood VARCHAR(30),
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            character_id INTEGER NOT NULL,
            role VARCHAR(20) NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP
        )
    ''')

    print('✅ Таблицы созданы в PostgreSQL!')
    cursor.close()
    conn.close()

except Exception as e:
    print(f'❌ Ошибка: {e}')