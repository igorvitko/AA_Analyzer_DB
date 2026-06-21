import os
import time
import requests

import settings
import database


def ensure_data_dir():
    """Создает папку для данных, если она отсутствует."""
    if not os.path.exists(settings.DATA_DIR):
        os.makedirs(settings.DATA_DIR)
        print(f"📁 Стоврена папка: {settings.DATA_DIR}")


def run_fetcher():
    """Загружаем данные по списку областей (UIDS_OBL)."""
    print(f"📡 Сінхронізація даних по областях: {settings.UIDS_OBL}")
    ensure_data_dir()
    database.init_db()
    cnt_loading = 0
    total_new = 0
    total_updated = 0
    for uid_obl in settings.UIDS_OBL:
        print(
            f"🔄 Загрузка даних області UID {uid_obl}... [{cnt_loading + 1}/{len(settings.UIDS_OBL)}]", end=" ", flush=True)
        url = f"https://api.alerts.in.ua/v1/regions/{uid_obl}/alerts/{settings.FETCH_PERIOD}.json?token={settings.API_TOKEN}"

        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                alerts_data = response.json().get('alerts', [])
                new_added, updated = database.save_alerts_to_db(alerts_data)
                total_new += new_added
                total_updated += updated
                cnt_loading += 1
                print(
                    f"OK. Нових записів: {new_added}, Закрито активних: {updated}")
            else:
                print(f"Помилка API {response.status_code}")
        except Exception as e:
            print(f"Помилка: {e}")

        if uid_obl != settings.UIDS_OBL[-1]:
            print("⏳ Пауза 45 сек...")
            time.sleep(45)

    print(
        f"✅ Сінхронізація завершена. Всього нових записів в базу: {total_new}, Оновлено: {total_updated}")
