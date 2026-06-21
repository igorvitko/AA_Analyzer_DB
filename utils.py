import argparse
import calendar
from datetime import date


def get_current_month_bounds():

    today = date.today()

    first_day = today.replace(day=1)

    return first_day, today


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


def str_to_bool(value):
    if isinstance(value, bool):
        return value
    if value.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif value.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Очікується значення True або False.')


def parse_arguments():

    parser = argparse.ArgumentParser(
        description="Щомісячний звіт часу повітрянних тревог.")

    parser.add_argument("-s", "--start", type=valid_date,
                        help="Дата початку звіту")
    parser.add_argument("-e", "--end", type=valid_date,
                        help="Дата кінця звіту")
    parser.add_argument("-r", "--run-db", type=str_to_bool, default=True,
                        help="Запускати скрипт загрузки БД? (True/False)")

    args = parser.parse_args()

    # Отримуємо дефолтні значення для поточного місяця
    default_start, default_end = get_current_month_bounds()

    start_date = args.start or default_start
    end_date = args.end or default_end

    if start_date > end_date:
        print("Помилка: Дата початку не може бути більшою за дату кінця!")
        exit(1)

    return start_date, end_date, args.run_db
