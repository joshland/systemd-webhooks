import os
import yaml
from loguru import logger

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'SUPER-SECRET'
    STARTUP_CONFIG = os.environ.get('STARTUP_CONFIG') or ''
    NOTICE_PATH = os.environ.get('NOTICE_PATH') or 'SUPER-SECRET'
    LOGFILE = "log.log"

    def __init__(self):
        global basedir
    
        logger.info('Config Init')
        if self.STARTUP_CONFIG:
            print("Startup")
            logger.trace(f'Loading Startup Config: {self.STARTUP_CONFIG}')
            with open(os.path.join(basedir,self.STARTUP_CONFIG), 'r') as cf:
                self.configfile = yaml.safe_load(cf)
                pass
            for k, v in self.configfile.items():
                print(f"Startup {k}")
                logger.info(f'Loaded {k}')
                self.__setattr__(k, v)
        else:
            logger.trace(f"No STARTUP_CONFIG")
        logger.info('Config Init')
        

class DevelopmentConfig(Config):
    DEBUG = True
    LOG_BACKTRACE = True
    LOG_LEVEL = 'DEBUG'
    CONFIG_FILE = 'dev.yaml'
    def __init__(self):
        super().__init__()

class ProductionConfig(Config):
    LOG_BACKTRACE = False
    LOG_LEVEL = 'INFO'
    CONFIG_FILE = 'prod.yaml'
    def __init__(self):
        super().__init__()


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

