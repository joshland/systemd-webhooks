import logging
import sys

from pathlib import Path
from flask import Flask
from loguru import logger

app = Flask(__name__)

class InterceptHandler(logging.Handler):
    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelname, record.getMessage())

def configure_logging(flask_app: Flask):
    path = Path(flask_app.config['LOG_PATH'])
    loglevel = Path(flask_app.config['LOG_LEVEL'])

    if not path.exists():
        path.mkdir(parents=True)
    log_name = Path(path, 'hooklog.log')


    logging.basicConfig(handlers=[InterceptHandler(level='INFO')], level=loglevel)
    logger.configure(handlers=[{"sink": sys.stderr, "level": loglevel}])
    logger.add(
        log_name, rotation="500 MB", encoding='utf-8', colorize=False, level=loglevel
    )   # this logs to file
