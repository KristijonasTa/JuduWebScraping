"""Main logging class"""
import logging

# pylint: disable=too-few-public-methods
class LogsClass:
    """Main logging class"""
    def __init__(self, log_level='info'):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(self.get_logging_level(log_level))

        file_handler = logging.FileHandler('./project_files/logs.log', 'w')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)

    def get_logging_level(self, log_level):
        """Set logging levels"""
        levels = {
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'warning': logging.WARNING,
            'error': logging.ERROR,
            'critical': logging.CRITICAL
        }
        return levels.get(log_level.lower(), logging.INFO)
