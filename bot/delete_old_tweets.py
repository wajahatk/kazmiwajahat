from os import getenv
from datetime import datetime, timedelta
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
def delete_old_tweets():
    #Delete tweets more than 5 days old
    days_to_keep = 5
    cutoff_date = datetime.now() - timedelta(days=days_to_keep)
    tweets_to_save = []
    print("¨…¨…¨Retrieving timeline tweets¨…¨…¨")
    try:
        try:
            timeline = Cursor(api.user_timeline).items()
        except TweepError as error:
            send_error_email(error)
            print(f"-> Error: {error.reason}")
        deletion_count = 0
        ignored_count = 0
        print(f"Cutoff date is: {cutoff_date}. The following tweets are being deleted:")
        print('xx--------------------------xx')
        for t in timeline:
            try:
                if t.id not in tweets_to_save and t.created_at < cutoff_date:
                    print(f"-> Deleted {t.id} created {t.created_at}")
                    api.destroy_status(t.id)
                    deletion_count += 1
                else:
                    ignored_count += 1
            except TweepError as error:
                send_error_email(error)
                print(f"-> Error: {error.reason}")
        print(f"¨…¨…¨Deleted {deletion_count} tweets from user-timeline¨…¨…¨")
        print(f"         ¨…¨…¨Ignored {ignored_count} tweets¨…¨…¨")
    except Exception as error:
        print(f"-> Error: {error}")
        send_error_email(error)
        pass

# ---------------------------------------------------------------------------- #
if __name__ == "__main__":
    delete_old_tweets()