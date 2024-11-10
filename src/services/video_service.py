from configparser import ConfigParser
from datetime import datetime
import datetime as dt
import logging

from repositories.videos.json_video_repository import JsonVideoRepository
from repositories.videos.csv_video_repository import CsvVideoRepository
from repositories.videos.gss_video_repository import GssVideoRepository

logger_pro = logging.getLogger('production')


class VideoService():
    """Video Service"""

    def __init__(self):
        config_file = 'config/config.ini'
        config = ConfigParser()
        config.read(config_file)

        self.json_repo = JsonVideoRepository()
        self.csv_repo = CsvVideoRepository()
        self.gss_repo = GssVideoRepository()

    def retrieve_videos(self) -> tuple:
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

            title_prefix = w["title"].split()[0]
            if title_prefix != "Watched":
                continue


            title = w['title'].lstrip("Watched ")

            if title == "Answered survey question":
                video_ads.append(w)
                continue

            channel = w['subtitles'][0]['name']
            url = w['titleUrl']
            # 2023-06-18T12:12:24.318Z -> 2023-06-18 12:12:24
            # 2023-06-12T21:33:12Z -> 2023-06-12 21:33:12
            timestamp_str = w['time'].replace("T", " ").strip("Z").split('.')[0]
            timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
            time_gap = dt.timedelta(hours=9)
            timestamp_jp = timestamp + time_gap

            videos.append([title, channel, url, timestamp_jp])

        logger_pro.info(f'videos: {len(videos)}')
        logger_pro.info(f'ads: {len(video_ads)}')
        logger_pro.info(f'unable: {len(videos_unable)}')

        return videos, video_ads, videos_unable

    def retrieve_new_videos(self, all_videos: list) -> list:
        # TODO: test case for if there is no data on csv

        # # get latest date
        latest_video = self.csv_repo.get_latest_video()

        if not latest_video:
            return all_videos

        latest_date_str = latest_video[0][4]
        latest_date = datetime.strptime(latest_date_str, '%Y-%m-%d %H:%M:%S')

        new_videos = []
        for v in all_videos:
            timestamp = v[3]
            if timestamp > latest_date:
                new_videos.append(v)

        return new_videos

    @classmethod
    def get_csv_next_id(cls, latest_video: list) -> int:
        if not latest_video:
            return 1

        return int(latest_video[0][0]) + 1

    @classmethod
    def get_gss_next_id(cls, ids: list) -> int:
        if len(ids) == 1:
            return 1

        return int(ids[-1]) + 1

    def add_new_videos(self, videos) -> None:
        lv = self.csv_repo.get_latest_video()
        csv_next_id = VideoService.get_csv_next_id(lv)

        header_gap = 1
        ids = self.gss_repo.retrieve_column_values(2)
        gss_next_id = VideoService.get_gss_next_id(ids)
        gss_next_empty_row = int(len(ids)) + header_gap

        for video in videos:
            video_to_csv = video.copy()
            video_to_csv.insert(0, csv_next_id)

            video_to_gss = video.copy()
            video_to_gss.insert(0, gss_next_id)

            self.csv_repo.add(video_to_csv)
            self.gss_repo.add(video_to_gss, gss_next_empty_row)

            csv_next_id += 1
            gss_next_id += 1
            gss_next_empty_row += 1
