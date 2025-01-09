"""
Все важные пути,
необходимые для нормального функционирования проекта.
"""

from pathlib import Path

_WORKDIR = Path(__file__).parent.parent.parent

LOG_DIR = _WORKDIR / "Logs"
LOCALE_DIR = _WORKDIR / "Mousey/Locales"
BOT_SETTINGS_DIR = _WORKDIR / "Mousey/Bot/"
CONFIG_FILE_PATH = _WORKDIR / ".env"
