import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    fmt="[with-mTLS] %(asctime)s - %(levelname)s : %(message)s",
    datefmt="%d/%m/%Y %I:%M:%S %p",
)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

file_handler = logging.FileHandler('with_mTLS.log')
file_handler.setFormatter(formatter)

logger.addHandler(handler)
logger.addHandler(file_handler)
