import logging
import json
import os


class __Config(object):
    def __init__(self):
        self.root_path = os.path.dirname(__file__)[:-len('tools')]
        logging.basicConfig(level=logging.ERROR,
                            format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                            filename=str(self.root_path + 'error.log'))
        self.logger = logging.getLogger(__name__)
        self.__load('info.json')

    def __load(self, file):
        try:
            with open(self.root_path + file, 'r') as f:
                self.info = json.loads(f.read())
        except Exception as e:
            self.info = {}
            self.logger.error(str(e))


config = __Config()
