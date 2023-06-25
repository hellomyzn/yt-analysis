from configparser import ConfigParser
from datetime import datetime
import json
import logging

logger_pro = logging.getLogger('production')

class SearchService(object):
    def __init__(self):
        config_file = 'config/config.ini'
        CONFIG = ConfigParser()
        CONFIG.read(config_file)

        self.search_history_path = CONFIG['PATH']['SEARCH_HISTORY']

    def retrieve_search_keywords(self):
        json_open = open(self.search_history_path, 'r')
        search_history_json_data = json.load(json_open)

        search_keywords = []
        search_ads = []

        for s in search_history_json_data:
            if 'details' in s:
                search_ads.append(s)
                continue

            # remove "Searched for " and space in the begining
            keyword = s['title'].strip('Searched for ').lstrip()
            # 2023-06-18T12:12:24.318Z -> 2023-06-18 12:12:24
            # 2023-06-12T21:33:12Z -> 2023-06-12 21:33:12
            timestamp_str = s['time'].replace("T", " ").strip("Z").split('.')[0]
            timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
            print(keyword,  timestamp)

            search_keywords.append([keyword, timestamp])

        return search_keywords, search_ads

