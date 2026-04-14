import data_fetcher
import alert_analyzer


def main():
    print("-" * 40)
    print("   СИСТЕМА НАКОПЛЕНИЯ И АНАЛИЗА ТРЕВОГ")
    print("-" * 40)

    # 1. Сначала скачиваем свежие данные из API и дописываем их в базу
    # (эту строку можно закомментировать, если данные уже в базе и нужно просто перестроить отчет)
    data_fetcher.run_fetcher()

    print("\n" + "=" * 40 + "\n")

    # 2. Формируем отчет на основе данных из базы за период в settings.py
    alert_analyzer.run_analysis()

    print("-" * 40)
    print("   ПРОЦЕСС ЗАВЕРШЕН")


if __name__ == "__main__":
    main()
