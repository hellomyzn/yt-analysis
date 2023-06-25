import csv
from configparser import ConfigParser
from datetime import datetime
import logging
from re import sub

logger_pro = logging.getLogger('production')

class SubscriptionService(object):

    def __init__(self):
        config_file = 'config/config.ini'
        CONFIG = ConfigParser()
        CONFIG.read(config_file)

        self.subscription_path = CONFIG['PATH']['SUBSCRIPTION_HISTORY']

    def retrieve_subscription(self):
        subsciption = []

        with open(self.subscription_path, 'r') as f:
            reader = csv.reader(f)
            # skip header
            next(reader)

            for row in reader:
                # sometimes there are some empty row
                if row:
                    status = True
                    channel = row[2]
                    url = row[1]
                    subsciption.append([status, 
                                        channel, 
                                        url, 
                                        datetime.now()])

        return subsciption
