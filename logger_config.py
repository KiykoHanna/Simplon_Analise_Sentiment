from loguru import logger
from pathlib import Path

# Папка для логов
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Файл логов
LOG_FILE = LOG_DIR / "app.log"

# Настройка логгера
logger.remove()
logger.add(
    LOG_FILE,
    rotation="5 MB",
    retention="10 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)
