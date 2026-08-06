# test_pg_simple.py
import asyncpg
import asyncio


async def test():
    try:
        # Пробуем разные варианты подключения
        print("🔍 Пробуем подключиться...")

        # Вариант 1: через localhost
        conn = await asyncpg.connect(
            user='friend',
            password='221096',
            database='virtual_friend',
            host='localhost',
            port=5432,
            timeout=10
        )
        print("✅ Подключение через localhost успешно!")
        await conn.close()
        return True

    except Exception as e:
        print(f"❌ Ошибка через localhost: {e}")

        try:
            # Вариант 2: через 127.0.0.1
            conn = await asyncpg.connect(
                user='friend',
                password='221096',
                database='virtual_friend',
                host='127.0.0.1',
                port=5432,
                timeout=10
            )
            print("✅ Подключение через 127.0.0.1 успешно!")
            await conn.close()
            return True
        except Exception as e2:
            print(f"❌ Ошибка через 127.0.0.1: {e2}")

            try:
                # Вариант 3: через host.docker.internal (для Windows)
                conn = await asyncpg.connect(
                    user='friend',
                    password='221096',
                    database='virtual_friend',
                    host='host.docker.internal',
                    port=5432,
                    timeout=10
                )
                print("✅ Подключение через host.docker.internal успешно!")
                await conn.close()
                return True
            except Exception as e3:
                print(f"❌ Ошибка через host.docker.internal: {e3}")
                return False


if __name__ == "__main__":
    result = asyncio.run(test())
    if result:
        print("\n🎉 Подключение работает!")
    else:
        print("\n❌ Не удалось подключиться ни через один хост")