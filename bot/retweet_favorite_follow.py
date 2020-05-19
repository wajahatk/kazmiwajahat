from os import getenv, system
from .waits.short_wait import short_wait
from .waits.med_wait import med_wait
from .waits.long_wait import long_wait
from .mailer.send_error_email import send_error_email
from tweepy import Cursor, TweepError, OAuthHandler, API
from .models import MentionsTweets


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
def retweet_favorite_follow(mention_list, people_i_follow):
    id_list = []
    #Get my screen name:
    me = api.me().screen_name
    #Get mentions from DB:
    mentions_in_db = MentionsTweets.query.all()
    #Loop thorugh mentions in db:
    for ment in mentions_in_db:
        id_list.append(ment.tweet)
    #Loop thorugh mention_list from args:
    for mention in reversed(mention_list):
        if mention.user.screen_name != me and mention.id not in id_list:
            try:
                #Reply to mention:
                api.update_status("Thanks for then mention, @" + mention.user.screen_name + ". I'll forward this to my creator, @jheeeeezy for you! Follow me in the meantime!", mention.id)
                api.create_favorite(mention.id)
                api.retweet(mention.id)
                short_wait.short_wait()
            except TweepError as error:
                print(f"-> Error: {error.reason}")
                send_error_email.send_error_email(error)
                pass
            except Exception as error:
                print(f"-> ERROR: {error}")
                send_error_email.send_error_email(att_error)
                pass
        if mention.user.id not in people_i_follow:
            try:
                api.create_friendship(mention.user.screen_name)
                print(f"-> Just followed @{mention.user.screen_name}!")
                short_wait.short_wait()
            except TweepError as error:
                print(f"-> Error: {error.reason}")
                send_error_email.send_error_email(error)
                pass
        short_wait.short_wait()
    #Update mentions in database:
    system('twitter-to-sqlite mentions-timeline twitter.db')
    print("Updated mentions db...")


# ---------------------------------------------------------------------------- #
if __name__ == "__main__":
    retweet_favorite_follow()