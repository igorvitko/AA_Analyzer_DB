import argparse

from data_fetcher import run_fetcher
from alert_analyzer import run_analysis
from utils import get_current_month_bounds, valid_date


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Щомісячний звіт часу повітрянних тревог.")

    parser.add_argument("-s", "--start", type=valid_date,
                        help="Дата початку звіту")
    parser.add_argument("-e", "--end", type=valid_date,
                        help="Дата кінця звіту")
    parser.add_argument("-r", "--run-db", type=lambda x: (str(x).lower() == 'true'),
                        default=True, help="Запускати скрипт загрузки БД? (True/False)")

    args = parser.parse_args()

    # Отримуємо дефолтні значення для поточного місяця
    default_start, default_end = get_current_month_bounds()

    start_date = args.start or default_start
    end_date = args.end or default_end

    if start_date > end_date:
        print("Помилка: Дата початку не може бути більшою за дату кінця!")
        exit(1)

    print("-" * 40)
    print("   СИСТЕМА НАКОПИЧЕННЯ ТА АНАЛИЗУ ЧАСУ ТРЕВОГ")
    print("-" * 40)

    # 1. На початку скачуємо нові дані з API и дописуємо їх в базу
    # (за замовченням оновлення даних відбвається, але є можливість його відключити, якщо потірбно тільки сформувати звіт)
    if args.run_db:
        print("Завантаження даних про повітряні тривоги в БД...")
        run_fetcher()
    else:
        print("Завантаження в БД скасовано користувачем.")

    print("\n" + "=" * 40 + "\n")

    # 2. Формируємо звіт на даних з бази за період вказаний користовачем, або дефолтно за поточний місяц
    run_analysis(start_date=start_date, end_date=end_date)

    print("-" * 40)
    print("== ПРОЦЕС ЗАВЕРШЕНО ==")
