import logging
import os
import sys
import uuid


def create_logger() -> logging.Logger:
    app_name = os.environ["APP_NAME"]
    new_logger = logging.getLogger(app_name)
    level = os.environ.get("LOG_LEVEL", logging.INFO)

    new_logger.setLevel(level)
    new_logger.propagate = False
    log_formatter = logging.Formatter(
        "[%(asctime)s] - [%(name)s] - [%(levelname)s] - [%(module)s:%(lineno)d]"
        " - %(message)s - [%(data_info)s]"
    )

    if not new_logger.handlers:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(log_formatter)
        new_logger.addHandler(console_handler)

    return new_logger


log = create_logger()
extra_info = {"identifier": str(uuid.uuid1())}
logger = logging.LoggerAdapter(log, extra={"data_info": extra_info})
