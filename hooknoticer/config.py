import os
import yaml
from loguru import logger

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'SUPER-SECRET'
    STARTUP_CONFIG = os.environ.get('STARTUP_CONFIG') or ''
    NOTICE_PATH = os.environ.get('NOTICE_PATH') or '/tmp'
    LOGFILE = "log.log"

class DevelopmentConfig(Config):
    DEBUG = True
    LOG_BACKTRACE = True
    LOG_LEVEL = 'DEBUG'
    CONFIG_FILE = 'dev.yaml'

class ProductionConfig(Config):
    LOG_BACKTRACE = False
    LOG_LEVEL = 'INFO'
    CONFIG_FILE = 'prod.yaml'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

