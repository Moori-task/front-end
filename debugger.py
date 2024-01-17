import logging
from singleton import Singleton


class Debugger(metaclass=Singleton):
    def __init__(self):
        # Enable logging
        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
        )
        # set higher logging level for httpx to avoid all GET and POST requests being logged
        logging.getLogger("httpx").setLevel(logging.WARNING)
        
        self.logger = logging.getLogger(__name__)

    def get_logger(self):
        return self.logger
    
Debugger()