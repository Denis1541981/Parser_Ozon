import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

class Logger:
    def __init__(self, name: str, log_file: str = "Ozone.log", level=logging.INFO):

        Path("Logs").mkdir(exist_ok=True)
        log_path = Path("Logs") / log_file


        log_format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        date_format = "%Y-%m-%d %H:%M:%S"


        handler = RotatingFileHandler(
            log_path, maxBytes=5_000_000, backupCount=3, encoding="utf-8"
        )


        logging.basicConfig(level=level, format=log_format, datefmt=date_format, filemode="a")
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)


        if not self.logger.handlers:
            self.logger.addHandler(handler)

    def info(self, msg: str):
        self.logger.info(msg)

    def warning(self, msg: str):
        self.logger.warning(msg)

    def error(self, msg: str):
        self.logger.error(msg)

    def debug(self, msg: str):
        self.logger.debug(msg)
