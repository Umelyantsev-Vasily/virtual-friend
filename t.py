import psycopg2
print("psycopg2 imported")
try:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        user="postgres",
        password="221096",
        database="virtual_friend"
    )
    print("Connected!")
    conn.close()
except Exception as e:
    print(f"Error: {e}")