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
    Если тревога уже существует, но ранее была без времени окончания (finished_at IS NULL),
    обновляет её актуальными данными с сервера.
    """
    conn = sqlite3.connect(settings.DB_PATH)
    cursor = conn.cursor()

    added_count = 0
    updated_count = 0

    for a in alerts_list:
        alert_id = a.get('id')
        finished_at = a.get('finished_at')

        # 1. Сначала проверяем, есть ли уже такая запись в базе
        cursor.execute(
            "SELECT finished_at FROM alerts WHERE id = ?", (alert_id,))
        row = cursor.fetchone()

        if row is None:
            # Записи нет — делаем обычную вставку
            cursor.execute('''
                INSERT INTO alerts 
                (id, location_uid, location_title, started_at, finished_at, alert_type, location_oblast, location_oblast_uid)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                alert_id,
                a.get('location_uid'),
                a.get('location_title'),
                a.get('started_at'),
                finished_at,
                a.get('alert_type'),
                a.get('location_oblast'),
                a.get('location_oblast_uid')
            ))
            added_count += 1
        else:
            # Запись есть. Проверяем, была ли она "открытой" (finished_at был пуст),
            # а теперь пришло время окончания.
            existing_finished_at = row[0]
            if (existing_finished_at is None or existing_finished_at == "") and finished_at is not None:
                cursor.execute('''
                    UPDATE alerts 
                    SET finished_at = ? 
                    WHERE id = ?
                ''', (finished_at, alert_id))
                updated_count += 1

    conn.commit()
    conn.close()

    # Возвращаем кортеж с количеством новых и обновленных записей для красивого лога
    return added_count, updated_count


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
