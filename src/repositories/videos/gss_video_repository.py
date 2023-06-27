import time
from configparser import ConfigParser
import logging

from google.oauth2.service_account import Credentials
import gspread

logger_pro = logging.getLogger('production')

class GssVideoRepository(object):
    def __init__(self):
        config_file = 'config/config.ini'
        CONFIG = ConfigParser()
        CONFIG.read(config_file)
        self.ws = GssVideoRepository.connect_gspread(
            CONFIG['GSPREAD']['JSONF_PATH'],
            CONFIG['GSPREAD']['SPREADSHEET_KEY'],
            CONFIG['GSPREAD']['SPREADSHEET_NAME_VIDEO'])
        self.sleep_time_sec = 0.8

    @classmethod
    def connect_gspread(cls, jsonf: str, key: str, sheet_name: str) -> gspread:
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        credentials = Credentials.from_service_account_file(jsonf, scopes=scopes)
        gc = gspread.authorize(credentials)
        SPREADSHEET_KEY = key
        worksheet = gc.open_by_key(SPREADSHEET_KEY).worksheet(sheet_name)

        return worksheet

    @classmethod
    def tail(cls, path: str, n: int) -> list:
        return []

    def get_all(self) -> list:
        return []

    def get_latest_video(self) -> list:
        latest_video = GssVideoRepository.tail(self.path, 1)
        return latest_video

    def retrieve_column_values(self, col: int) -> list:
        cols = list(filter(None, self.ws.col_values(col)))
        return cols

    def add(self, video: list, row: int) -> None:

        for col, value in enumerate(video, start=2):
            self.ws.update_cell(row, col, str(value))
            time.sleep(self.sleep_time_sec)

        return None

