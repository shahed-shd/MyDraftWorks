import logging
from pathlib import Path
from .log import Log
from typing import Final


def get_log_dir_path() -> Path:
    base_dir_path: Path = Path(__file__).resolve().parent.parent
    log_dir_path: Path = Path(base_dir_path, 'logs')
    log_dir_path.mkdir(parents=True, exist_ok=True)
    return log_dir_path


def prepare_logger() -> logging.Logger:
    LOGGER_NAME: Final[str] = 'system_stats'
    log: Final[Log] = Log(logger_name=LOGGER_NAME, level=logging.DEBUG)

    log.add_console_handler()

    log_dir_path: Path = get_log_dir_path()
    log_file_path: Path = Path(log_dir_path, LOGGER_NAME + '.log')

    log.add_persistent_log_handler(level=logging.DEBUG, filename=log_file_path)

    return log.logger


logger: logging.Logger = prepare_logger()
