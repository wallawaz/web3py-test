import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%b %d %Y %H:%M:%S.%f'
)

LOGGER = logging.getLogger()
