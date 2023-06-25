from configparser import ConfigParser
from datetime import datetime
import logging

from repositories.videos.json_video_repository import JsonVideoRepository
from repositories.videos.csv_video_repository import CsvVideoRepository

logger_pro = logging.getLogger('production')

class VideoService(object):

    def __init__(self):
        config_file = 'config/config.ini'
        CONFIG = ConfigParser()
        CONFIG.read(config_file)

        self.json_repo = JsonVideoRepository()
        self.csv_repo = CsvVideoRepository()


    def retrieve_videos(self) -> list:
        # get json video data

        watch_history_json_data = self.json_repo.get_all()

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

        logger_pro.info(f'videos: {len(videos)}')
        logger_pro.info(f'ads: {len(video_ads)}')
        logger_pro.info(f'unable: {len(videos_unable)}')

        return videos, video_ads, videos_unable

    def retrieve_new_videos(self, all_videos: list) -> list:

        # # get latest date
        latest_video = self.csv_repo.get_latest_video()
        latest_date_str = latest_video[0][4]
        latest_date = datetime.strptime(latest_date_str, '%Y-%m-%d %H:%M:%S')
        print(latest_date)

        # new videos
        new_videos = []
        for i, v in enumerate(all_videos):
            timestamp = v[3]
            if timestamp > latest_date:
                new_videos.append(v)

        return new_videos

