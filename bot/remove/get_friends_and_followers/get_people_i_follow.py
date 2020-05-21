from os import getenv
from .mailer import send_error_email
from tweepy import Cursor, TweepError, API, OAuthHandler


# ---------------------------------------------------------------------------- #
# API key:
api_key = getenv("CONSUMER_KEY")
# API secret key:
api_secret = getenv("CONSUMER_SECRET")
# Access token: 
access_token = getenv("API_KEY")
# Access token secret: 
access_token_secret = getenv("API_SECRET")
# ---------------------------------- Tweepy ---------------------------------- #
# Tweepy 0Auth 1a authentication:
auth = OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)
# API Variable:
api = API(auth, wait_on_rate_limit=True)


# ---------------------------------------------------------------------------- #
def get_people_i_follow():
    try:
        following = api.friends()
    except TweepError as error:
        print(f"-> Error: {error.reason}")
        send_error_email.send_error_email(error)
        pass
    following_id_list = []
    try:
        for page in Cursor(api.friends_ids).pages():
            following_id_list.extend(page)
        return following_id_list
    except TweepError as error:
        print(f"-> Error: {error.reason}")
        send_error_email.send_error_email(error)
        pass


# ---------------------------------------------------------------------------- #
if __name__ == "__main__":
    get_people_i_follow()