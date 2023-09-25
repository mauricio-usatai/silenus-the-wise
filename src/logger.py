import logging

LOGGERS = {}


def create_logger(name="mylog"):
    """Call logger and handle with multiples stdout."""
    if LOGGERS.get(name):
        return LOGGERS.get(name)
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "{asctime} {threadName:>11} {levelname} {message}", style="{"
    )

    # Log to stdout too
    streamhandler = logging.StreamHandler()
    streamhandler.setLevel(logging.INFO)
    streamhandler.setFormatter(formatter)
    log.addHandler(streamhandler)
    LOGGERS[name] = log
    return log
