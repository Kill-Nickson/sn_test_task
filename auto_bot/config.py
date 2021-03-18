from os.path import exists
from configparser import ConfigParser, NoSectionError, NoOptionError


class Config:

    def __init__(self, path='./configs/config.ini'):
        self.max_likes_per_user = None
        self.max_posts_per_user = None
        self.number_of_users = None
        self.path = path

        self.init_vars()

    def init_vars(self):
        config = ConfigParser()

        if not exists(self.path):
            print('Config file not found!')
            exit()

        config.read(self.path)
        try:
            self.max_likes_per_user = config.get('Variables', 'max_likes_per_user')
            self.max_posts_per_user = config.get('Variables', 'max_posts_per_user')
            self.number_of_users = config.get('Variables', 'number_of_users')
        except NoSectionError:
            print('NoSectionError occurred while reading config!')
        except NoOptionError:
            print('NoOptionError occurred while reading config!')
