from datetime import timedelta
from loguru import logger


logger.add(
    "./logs/{time}.log",
    format="{time:HH:mm:ss} | {level} | {message}",
    enqueue=True,
    retention=timedelta(days=7),
)
