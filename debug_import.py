import traceback
import sys
sys.path.insert(0, '.')

try:
    import test_sync_db
    print("✅ test_sync_db imported successfully")
except Exception as e:
    traceback.print_exc()
    # Находим файл, где произошла ошибка
    tb = e.__traceback__
    while tb:
        print(f"File: {tb.tb_frame.f_code.co_filename}, Line: {tb.tb_lineno}")
        tb = tb.tb_next