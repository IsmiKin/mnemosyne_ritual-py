import logging


def get_logger():
    """Initialize and return a logger instance."""
    FORMAT = "[%(asctime)s][%(levelname)-5.5s] %(message)s"
    logging.basicConfig(format=FORMAT)
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    return log
