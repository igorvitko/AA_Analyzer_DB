import os
from datetime import time, date
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# --- API НАСТРОЙКИ ---
# Токен берется из .env (переменная TOKEN)
API_TOKEN = os.environ.get('TOKEN', 'ВАШ_ТОКЕН_ПО_УМОЛЧАНИЮ')
FETCH_PERIOD = 'month_ago'

# --- ПУТИ И ФАЙЛЫ ---
DATA_DIR = "data"  # Папка для хранения db
REPORTS_DIR = "reports"  # Папка для хранения отчетов
OUTPUT_FILE = f"{REPORTS_DIR}/air_raid_working_hours.xlsx"
DB_PATH = f"{DATA_DIR}/alerts_history.db"

# --- ВРЕМЕННЫЕ ЗОНЫ ---
# Смещение времени (например, +3 для Киева, если в API данные в UTC)
TIME_OFFSET_HOURS = 3

# --- ПРАВИЛА ВЫБОРКИ ---
# Список интересующих кодов location_uid
UIDS_OBL = [3, 4, 5, 8, 9, 11, 12, 13, 15, 17, 18, 19,
            21, 22, 24, 25, 26, 27, 31]
TARGET_LOCATIONS = [36, 44, 68, 31, 81, 39, 90, 98, 104,
                    101, 109, 112, 119, 66, 134, 152, 140, 137, 564, 1293]

# рабочий график и обед
WORK_START = time(9, 0)
WORK_END = time(17, 30)
LUNCH_START = time(13, 0)
LUNCH_END = time(14, 0)

# тип тревоги
ALERT_TYPE = "air_raid"


# --- ПЕРИОД ДЛЯ ОТЧЕТА EXCEL ---
# Здесь вы указываете даты, за которые хотите построить таблицу из накопленных данных
REPORT_START_DATE = date(2026, 4, 1)
REPORT_END_DATE = date(2026, 4, 30)
