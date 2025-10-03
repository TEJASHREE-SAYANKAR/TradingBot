import logging
import sys
from logging.handlers import RotatingFileHandler
from bot.config import LOGFILE

logger = logging.getLogger("BinanceBot")
logger.setLevel(logging.DEBUG)

# Console handler

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)

# Rotating file handler

fh = RotatingFileHandler(LOGFILE, maxBytes=5 * 1024 * 1024, backupCount=3)
fh.setLevel(logging.DEBUG)
fh_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
fh.setFormatter(fh_formatter)
logger.addHandler(fh)
