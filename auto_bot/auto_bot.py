from random import randint, shuffle
import requests

from database import Database


class Bot:

    def __init__(self, number_of_users, max_posts_per_user, max_likes_per_user):
        self.number_of_users = int(number_of_users)
        self.max_posts_per_user = int(max_posts_per_user)
        self.max_likes_per_user = int(max_likes_per_user)
        self.bots = []
        self.bot_tokens = []

    def signup_accounts(self):
        print('Signing up bots:')
        signup_endpoint = 'http://127.0.0.1:8000/auth/users/'
        headers = {'Content-Type': 'application/json'}

        for i in range(self.number_of_users):
            while True:
                while True:
                    random_bot_id = str(randint(1, 1_000_000_000))
                    email = 'bot' + random_bot_id + '@gmail.com'
                    if self._verify_email(email):
                        break
                username = 'bot' + random_bot_id
                password = 'qwerty24Qq'
                signup_response = requests.post(signup_endpoint, headers=headers,
                                                json={
                                                    "email": email,
                                                    "username": username,
                                                    "date_of_birth": "1998-11-24",
                                                    "password": password
                                                }).json()
                if signup_response.get("username"):
                    if signup_response["username"] != "A user with that username already exists.":
                        self.bots.append([email, password])
                        print('\tSigned up', username)
                        break
        Database().table_update(self.bots)

    def publish_posts(self):
        print('Posts publishing:')
        for bot in self.bots:
            jwt = self._get_bot_jwt(bot)
            print('\tBot (' + jwt[-10:] + '...) is publishing posts...')
            self.bot_tokens.append(jwt)

            create_post_endpoint = 'http://127.0.0.1:8000/api/create/'
            headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + jwt}

            for _ in range(randint(1, self.max_posts_per_user)):
                requests.post(create_post_endpoint,
                              headers=headers,
                              json={
                                  "title": 'Random title', "body": 'Random body'
                              }).json()

    def like_posts(self):
        print('Posts "liking":')
        for jwt in self.bot_tokens:
            all_posts = [post_id['id'] for post_id in requests.get('http://127.0.0.1:8000/api/').json()]

            if self.max_likes_per_user < len(all_posts):
                max_posts_for_likes = randint(1, self.max_likes_per_user)
            else:
                max_posts_for_likes = self.max_likes_per_user

            shuffle(all_posts)
            random_posts = all_posts[:max_posts_for_likes]

            headers = {'Content-Type': 'application/json',
                       'Authorization': 'Bearer ' + jwt}

            for post_id in random_posts:
                requests.put('http://127.0.0.1:8000/api/update/' + str(post_id) + '/',
                             headers=headers,
                             json={"liked": True})
                print("\t Bot liked post with id", post_id)

    @staticmethod
    def _get_bot_jwt(bot):
        token_endpoint = 'http://127.0.0.1:8000/api/token/'
        headers = {'Content-Type': 'application/json'}
        email, password = bot[0], bot[1]
        auth_response = requests.post(token_endpoint,
                                      headers=headers,
                                      json={
                                          "email": email,
                                          "password": password,
                                      }).json()
        jwt = auth_response['access']
        return jwt

    @staticmethod
    def _verify_email(email):
        verify_response = requests.get(f'https://api.hunter.io/v2/email-verifier?email={email}&'
                                       'api_key=94f7fd50b62d79c9748976b374a91906630eb1a4').json()

        if verify_response['data']['status'] != 'invalid':
            return True
        return False
