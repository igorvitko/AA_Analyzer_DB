import argparse
import calendar

from datetime import date 


def get_current_month_bounds():
    today = date.today()
    # Перше число поточного місяця — це завжди 1-й день
    first_day = date(today.year, today.month, 1)

    # calendar.monthrange повертає кортеж (день_тижня, кількість_днів_у_місяці)
    _, last_day_num = calendar.monthrange(today.year, today.month)
    last_day = date(today.year, today.month, last_day_num)

    return first_day, last_day


def valid_date(date_string: str) -> date:
    if date_string is None:
        return None

    try:
        # return datetime.strptime(date_string, "%Y-%m-%d").date()
        return date.fromisoformat(date_string)
    except:
        raise argparse.ArgumentTypeError(
            f"Невірний формат дати: {date_string}. Потрібно ДД.ММ.РРРР."
        )
