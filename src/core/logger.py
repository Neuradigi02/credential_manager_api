import asyncio
import logging
import os
from logging.handlers import TimedRotatingFileHandler
from src.core.load_config import config


LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Set up a timed rotating file handler (new log file each day)
log_handler = TimedRotatingFileHandler(
    filename=LOG_FILE,  # Log file path
    when="midnight",  # Rotate at midnight
    interval=1,  # Rotate every day
    backupCount=30,  # Keep last 7 days of logs
    encoding="utf-8"
)

# Define log format
log_formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)
log_handler.setFormatter(log_formatter)

# Create and configure logger
logger = logging.getLogger()  # Custom logger name
logger.setLevel(logging.INFO if config["IsDevelopment"] else logging.WARNING)  # Log INFO level and above
logger.addHandler(log_handler)
logger.propagate = False  # Prevent duplicate logs

# Log startup message
# logger.info("Logging setup complete")

async def log_async(func, message):
    return await asyncio.to_thread(func, message)
