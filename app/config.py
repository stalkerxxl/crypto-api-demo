import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent

FMP_API_KEY = os.getenv('FMP_API_KEY')
FMP_API_URL = os.getenv('FMP_API_URL')

DB_URL = f'sqlite:///{BASE_DIR}/db/database.sqlite'
DB_DEBUG = bool(os.getenv('DB_DEBUG'))

LOG_LEVEL = os.getenv('LOG_LEVEL')
LOG_FOLDER = f'../{os.getenv('LOG_FOLDER')}'
APP_DEBUG = bool(int(os.getenv('APP_DEBUG', 0)))
######
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_ACCESS_TIME = int(os.getenv('JWT_ACCESS_TIME'))
JWT_REFRESH_TIME = int(os.getenv('JWT_REFRESH_TIME'))
