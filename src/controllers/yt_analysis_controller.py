import logging
from configparser import ConfigParser

from utils.logger import Logger
from services.video_service import VideoService
from services.search_keyword_service import SearchKeywordService
from services.subscription_service import SubscriptionService

logger_pro = logging.getLogger('production')


class YtAnalysisController(object):
    def __init__(self):
        config_file = 'config/config.ini'
        self.config = ConfigParser()
        self.config.read(config_file)

    def update(self):
        """update"""

        Logger().setup_logging(self.config['LOG']['LOG_CONFIG_PATH'])
        logger_pro.info('Start app')

        # retrieve new video data
        vs = VideoService()
        videos, video_ads, videos_unable = vs.retrieve_videos()
        del video_ads
        del videos_unable

        new_videos = vs.retrieve_new_videos(videos)
        if new_videos:
            vs.add_new_videos(new_videos)
        else:
            print("there is no new videos")

        # get search data
        sks = SearchKeywordService()
        search_keywords, search_ads = sks.retrieve_search_keywords()
        del search_ads
        del search_keywords

        # get subscirpiton data
        ss = SubscriptionService()
        subscription = ss.retrieve_subscription()
        del subscription
