import os
import datetime
from logging import getLogger, StreamHandler, DEBUG, FileHandler


def set_logger():
    # Log設定
    logger = getLogger(__name__)
    handler = StreamHandler()
    handler.setLevel(DEBUG)
    logger.setLevel(DEBUG)
    START_DATETIME = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    fh = FileHandler(os.path.join(os.path.dirname(__file__),
                                  'log', START_DATETIME+'.log'), encoding='utf-8')
    logger.addHandler(handler)
    logger.addHandler(fh)
    logger.propagate = False

    return logger
