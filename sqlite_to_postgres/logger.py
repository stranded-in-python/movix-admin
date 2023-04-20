import logging


def logger():
    logging.basicConfig(
        filename='logs.log', 
        level=logging.INFO,
        format="%(funcName)s | %(levelname)s | %(message)s"
    )
    logger = logging.getLogger(__file__)
    return logger
