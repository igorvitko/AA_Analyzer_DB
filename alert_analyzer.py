import os
import pandas as pd
from datetime import datetime, timedelta
import settings
import database


def ensure_report_dir():
    """Создает папку для отчета, если она отсутствует."""
    if not os.path.exists(settings.REPORTS_DIR):
        os.makedirs(settings.REPORTS_DIR)
        print(f"📁 Створена папка: {settings.REPORTS_DIR}")


def calculate_overlap_minutes(start_dt, end_dt, day_date):
    """Считает минуты тревоги внутри рабочего дня (с учетом обеда)."""
    if day_date.weekday() >= 5:  # Суббота и Воскресенье
        return 0

    # Границы рабочего времени для конкретного дня
    w_start = datetime.combine(day_date, settings.WORK_START)
    w_end = datetime.combine(day_date, settings.WORK_END)
    l_start = datetime.combine(day_date, settings.LUNCH_START)
    l_end = datetime.combine(day_date, settings.LUNCH_END)

    intervals = [(w_start, l_start), (l_end, w_end)]
    total_mins = 0

    for i_start, i_end in intervals:
        overlap_start = max(start_dt, i_start)
        overlap_end = min(end_dt, i_end)
        if overlap_start < overlap_end:
            total_mins += (overlap_end - overlap_start).total_seconds() / 60

    return total_mins


def run_analysis(start_date, end_date):
    """Формирует отчет на основе данных в базе."""
    print(
        f"📊 Формуємо звіт за період: {start_date} — {end_date}")

    ensure_report_dir()

    df = database.get_alerts_for_report(
        start_date, end_date)

    if df.empty:
        print("❌ В БД немає даних за цей період або по цих регіонах.")
        return

    processed_data = []

    for _, row in df.iterrows():
        # Применяем временное смещение
        start_dt = pd.to_datetime(row['started_at']).tz_localize(
            None) + timedelta(hours=settings.TIME_OFFSET_HOURS)
        end_dt = pd.to_datetime(row['finished_at']).tz_localize(
            None) + timedelta(hours=settings.TIME_OFFSET_HOURS)

        # Разбиваем тревогу на дни
        current_day = start_dt.date()
        while current_day <= end_dt.date():
            # Учитываем только те дни, которые входят в запрашиваемый период отчета
            if start_date <= current_day <= end_date:
                minutes = calculate_overlap_minutes(
                    start_dt, end_dt, current_day)
                if minutes >= 0:
                    processed_data.append({
                        'Reg_UID': int(row['location_uid']),
                        'Регіон': row['location_title'],
                        'Дата': current_day,
                        'Хвилини': minutes
                    })
            current_day += timedelta(days=1)

    if not processed_data:
        print("🛑 За вказаний період тревог в рабочий час не знайдено.")
        return

    # Создание финальной таблицы
    result_df = pd.DataFrame(processed_data)
    # Группируем по региону и дате (если было несколько тревог в день)
    summary = result_df.groupby(['Reg_UID', 'Регіон', 'Дата'])[
        'Хвилини'].sum().reset_index()

    # Разворачиваем в таблицу (строки - регионы, колонки - даты)
    pivot = summary.pivot_table(
        index=['Reg_UID', 'Регіон'], columns='Дата', values='Хвилини', fill_value=0)

    # Переводим в формат Excel Time (1 минута = 1 / 1440 суток)
    pivot_excel = pivot / 1440

    with pd.ExcelWriter(settings.OUTPUT_FILE, engine='openpyxl') as writer:
        pivot_excel.to_excel(writer, sheet_name='Отчет по тревогам')
        ws = writer.sheets['Отчет по тревогам']

        # Установка формата времени [ч]:мм для ячеек
        for row in ws.iter_rows(min_row=2, min_col=2):
            for cell in row:
                cell.number_format = '[h]:mm'

    print(f"✨ Звіт успішно сформовано: {settings.OUTPUT_FILE}")
