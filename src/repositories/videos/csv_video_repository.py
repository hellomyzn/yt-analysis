import csv
from configparser import ConfigParser
import logging

logger_pro = logging.getLogger('production')

class CsvVideoRepository(object):
    def __init__(self):
        config_file = 'config/config.ini'
        CONFIG = ConfigParser()
        CONFIG.read(config_file)
        self.path = CONFIG['PATH']['VIDEO_CSV']

    @classmethod
    def tail(cls, path: str, n: int) -> list:
        with open(path, 'r') as f:
            # skip header
            f.readline()
            # read all
            lines = f.readlines()
            tail_lines = []
            for line in lines[-n:]:
                l = list(line.strip().split(','))
                tail_lines.append(l)

        return tail_lines


    def get_all(self) -> list:
        return []

    def get_latest_video(self) -> list:
        latest_video = CsvVideoRepository.tail(self.path, 1)
        return latest_video
