from config import Config
from auto_bot import Bot


def main():
    config = Config()

    bot = Bot(number_of_users=config.number_of_users,
              max_posts_per_user=config.max_posts_per_user,
              max_likes_per_user=config.max_likes_per_user)
    bot.signup_accounts()
    bot.publish_posts()
    bot.like_posts()


if __name__ == '__main__':
    main()
