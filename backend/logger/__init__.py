from functools import lru_cache
import datetime
import logging


logging.basicConfig(format=f"%(datetime)s UTC [0] LOG: %(message)s", level=logging.INFO, force=True)


@lru_cache
def getLogger(module: str) -> logging.Logger:
    logger = logging.getLogger(module)

    def function(func):
        return lambda message: func(
            message,
            extra={"datetime": datetime.datetime.now()}
        ) 

    logger.info = function(logger.info)
    logger.warning = function(logger.warning)
    logger.error = function(logger.error)

    return logger
