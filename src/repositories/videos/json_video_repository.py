import json
from configparser import ConfigParser
import logging

logger_pro = logging.getLogger('production')

class JsonVideoRepository(object):
    def __init__(self):
        config_file = 'config/config.ini'
        CONFIG = ConfigParser()
        CONFIG.read(config_file)
        self.watch_history_path = CONFIG['PATH']['WATCH_HISTORY']

    def get_all(self) -> list:
        json_open = open(self.watch_history_path, 'r')
        watch_history_json_data = json.load(json_open)
        watch_history_json_data.reverse()

        return watch_history_json_data

