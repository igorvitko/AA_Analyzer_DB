import sqlite3
import pandas as pd
import settings


def init_db():
    """Инициализация базы данных и таблицы."""
    conn = sqlite3.connect(settings.DB_PATH)
    cursor = conn.cursor()
    # Мы используем id с сервера как PRIMARY KEY для предотвращения дубликатов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY,
            location_uid TEXT,
            location_title TEXT,
            started_at TEXT,
            finished_at TEXT,
            alert_type TEXT,
            location_oblast TEXT,
            location_oblast_uid INTEGER
        )
    ''')
    conn.commit()
    conn.close()


def save_alerts_to_db(alerts_list):
    """
    Сохраняет список тревог в базу. 
    Использует INSERT OR IGNORE, чтобы не дублировать записи по серверному id.
    """
    conn = sqlite3.connect(settings.DB_PATH)
    cursor = conn.cursor()

    added_count = 0
    for a in alerts_list:
        # Пытаемся вставить запись. Если id уже есть, SQLite её проигнорирует.
        cursor.execute('''
            INSERT OR IGNORE INTO alerts 
            (id, location_uid, location_title, started_at, finished_at, alert_type, location_oblast, location_oblast_uid)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            a.get('id'),  # Используем ID с сервера
            a.get('location_uid'),
            a.get('location_title'),
            a.get('started_at'),
            a.get('finished_at'),
            a.get('alert_type'),
            a.get('location_oblast'),
            a.get('location_oblast_uid')
        ))
        if cursor.rowcount > 0:
            added_count += 1

    conn.commit()
    conn.close()
    return added_count


def get_alerts_for_report(start_date, end_date):
    """Загружает данные из базы, отфильтрованные по региону и датам.
        Выбираем только те записи, UID которых входит в TARGET_LOCATIONS."""
    conn = sqlite3.connect(settings.DB_PATH)
    s_date = start_date.strftime('%Y-%m-%d')
    e_date = end_date.strftime('%Y-%m-%d')

    # Фильтрация по списку мелких территорий (TARGET_LOCATIONS)
    placeholders = ','.join(['?'] * len(settings.TARGET_LOCATIONS))
    query = f"""
        SELECT * FROM alerts 
        WHERE location_uid IN ({placeholders})
        AND date(started_at) <= ? 
        AND (finished_at IS NOT NULL AND date(finished_at) >= ?)
        AND alert_type = ?
    """
    params = list(settings.TARGET_LOCATIONS) + \
        [e_date, s_date, settings.ALERT_TYPE]

    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df
