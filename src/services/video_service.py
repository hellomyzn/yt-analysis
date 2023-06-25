from configparser import ConfigParser
from datetime import datetime
import json
import logging

logger_pro = logging.getLogger('production')

class VideoService(object):

    def __init__(self):
        config_file = 'config/config.ini'
        CONFIG = ConfigParser()
        CONFIG.read(config_file)

        self.watch_history_path = CONFIG['PATH']['WATCH_HISTORY']


    def retrieve_videos(self) -> list:
        # get json video data
        json_open = open(self.watch_history_path, 'r')
        watch_history_json_data = json.load(json_open)

        # retreive specific data
        videos = []
        video_ads = []
        videos_unable = []

        for w in watch_history_json_data:
            if 'details' in w:
                video_ads.append(w)
                continue

            if not 'subtitles' in w:
                videos_unable.append(w)
                continue

            title = w['title']
            channel = w['subtitles'][0]['name']
            url = w['titleUrl']
            # 2023-06-18T12:12:24.318Z -> 2023-06-18 12:12:24
            # 2023-06-12T21:33:12Z -> 2023-06-12 21:33:12
            timestamp_str = w['time'].replace("T", " ").strip("Z").split('.')[0]
            timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')

            videos.append([title, channel, url, timestamp])

        # sort by old one
        videos.reverse()

        logger_pro.info(f'videos: {len(videos)}')
        logger_pro.info(f'ads: {len(video_ads)}')
        logger_pro.info(f'unable: {len(videos_unable)}')

        return videos, video_ads, videos_unable
    
