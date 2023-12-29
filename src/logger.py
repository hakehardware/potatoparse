import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)