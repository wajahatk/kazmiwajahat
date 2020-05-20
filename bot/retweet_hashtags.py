from os import getenv
from random import shuffle
from .waits import short_wait, med_wait
from .mailer import send_error_email
from tweepy import Cursor, TweepError, OAuthHandler, API


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
hashtags = [
    '#dc',
    '#sanfrancisco',
    '#la',
    '#ny',
    '#webdevelopment', 
    '#skateboarding',
    '#WashingtonDC',
    '#sanfrancisco',
    '#losangeles',
    '#dmvmusic', 
    '#coding', 
    '#100daysofcode',
    '#dcrestaurant',
    '#sfrestaurant',
    '#larestaurant',
    '#nyrestaurant',
    '#gamedev',
    '#dcevents',
    '#sfevents',
    '#laevents',
    '#nyevents',
    '#dcnightlife',
    '#lanightlife',
    '#sfnightlife',
    '#nynightlife',
    '#ufc',
    '#gamingnews',
    '#newmusic',
    '#ustreetdc',
]

# ---------------------------------------------------------------------------- #
def retweet_hashtags(hashtag_list):
    shuffle(hashtag_list)
    for hashtag in hashtag_list:
        tweetNumber = 1
        try:
            tweets = Cursor(api.search, hashtag).items(tweetNumber)
            for tweet in tweets:
                try:
                    tweet.retweet()
                    print("-> Retweet Done!")
                    short_wait.short_wait()
                except TweepError as error:
                    print(error.reason)
                    send_error_email.send_error_email(error)
                    pass
                med_wait.med_wait()
        except TweepError as error:
            print(f"-> ERROR: {error.reason}")
            send_error_email.send_error_email(error)
            pass


# ---------------------------------------------------------------------------- #
if __name__ == "__main__":
    retweet_hashtags(hashtags)