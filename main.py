
from data_fetcher import run_fetcher
from alert_analyzer import run_analysis
from utils import parse_arguments


def main():

    start_date, end_date, run_db = parse_arguments()

    print("-" * 40)
    print("   СИСТЕМА НАКОПИЧЕННЯ ТА АНАЛИЗУ ЧАСУ ТРЕВОГ")
    print("-" * 40)

    # 1. На початку скачуємо нові дані з API и дописуємо їх в базу
    # (за замовченням оновлення даних відбвається, але є можливість його відключити, якщо потірбно тільки сформувати звіт)
    if run_db:
        print("Завантаження даних про повітряні тривоги в БД...")
        run_fetcher()
    else:
        print("Завантаження в БД скасовано користувачем.")

    print("\n" + "=" * 40 + "\n")

    # 2. Формируємо звіт на даних з бази за період вказаний користовачем, або дефолтно за поточний місяц
    run_analysis(start_date=start_date, end_date=end_date)

    print("-" * 40)
    print("== ПРОЦЕС ЗАВЕРШЕНО ==")


if __name__ == "__main__":
    main()
