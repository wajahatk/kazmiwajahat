from time import sleep
from os import getenv, system
from .models import Mention, db
from .waits.med_wait import med_wait
from .waits.long_wait import long_wait
from .waits.short_wait import short_wait
from sqlalchemy.exc import IntegrityError
from .mailer.send_error_email import send_error_email
from tweepy import Cursor, TweepError, OAuthHandler, API
from .get_friends_and_followers.get_my_followers import get_my_followers
from .get_friends_and_followers.get_people_i_follow import get_people_i_follow


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


def create_mention_db():
    #Create DB
    try:
        system('python bot/mentions/models.py db init')
        sleep(2)
    except:
        pass
    #Migrate
    try:
        system('python bot/mentions/models.py db migrate')
        sleep(2)
    except:
        pass
    #create table & db:
    db.create_all()
    sleep(2)



def refresh_mentions_db():
    create_mention_db()
    me = api.me().id
    mentions = api.mentions_timeline()
    for m in mentions:
        for k,v in m.__dict__.items():
            if m.id != me:
                new_mention = Mention(mention_id=m.id, sender=m.author.id, created=m.created_at)
                try:
                    db.session.add(new_mention)
                    db.session.commit()
                except IntegrityError as error:
                    db.session.rollback()



if __name__ == "__main__":
    refresh_mentions_db()