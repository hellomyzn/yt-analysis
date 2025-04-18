import csv
from configparser import ConfigParser
import logging
from config import CSV_DIR_PATH

logger_pro = logging.getLogger('production')

class CsvVideoRepository(object):
    def __init__(self):
        config_file = 'config/config.ini'
        CONFIG = ConfigParser()
        CONFIG.read(config_file)
        self.path = f"{CSV_DIR_PATH}/videos.csv"

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


    def add(self, video: int) -> None:
        with open (self.path, 'a', encoding='utf_8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(video)
        return None


