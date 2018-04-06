import logging

from graphene_boilerplate.config import LOGGER_NAME, DEBUG


logger = logging.getLogger(LOGGER_NAME)
if DEBUG:
    loglevel = logging.DEBUG
else:
    loglevel = logging.INFO

logging.basicConfig(level=loglevel, format='[%(asctime)s] [%(process)d] [%(levelname)s] [%(filename)s @ %(lineno)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S %z')
