from random import choice
from string import digits
from datetime import datetime
from os import getenv, system
from .models import Mention, db
from .waits.med_wait import med_wait
from .waits.long_wait import long_wait
from .waits.short_wait import short_wait
from sqlalchemy.exc import IntegrityError
from .mailer.send_error_email import send_error_email
from tweepy import Cursor, TweepError, OAuthHandler, API
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

def id_generator(size=6, chars=digits):
        return ''.join(choice(chars) for x in range(size))

def get_mention_ids_from_twitter():
    mention_tl = [m.id for m in api.mentions_timeline()]
    return mention_tl

def get_mentions_from_db():
    mentions_in_db = [m.mention_id for m in Mention.query.all()]
    return mentions_in_db

def get_info(id):
    mention = api.get_status(id)
    info = dict([('mention_id', mention.id), ('sender_id', mention.author.id), ('sender_sn', mention.author.screen_name), ('date', mention.created_at)])
    return info

def add_to_db(id):
    me = api.me().id
    mention = api.get_status(id)
    if mention.author.id != me:
        new_mention = Mention(mention_id=mention.id, sender=mention.author.id, created=mention.created_at)
        try:
            db.session.add(new_mention)
            db.session.commit()
            print(f"-> Mention {mention.id} added to db!")
        except IntegrityError as error:
            print(f"-> {mention.id} not added.")
            db.session.rollback()
        

def retweet_favorite_follow():
    me = api.me().id
    people_i_follow = get_people_i_follow()
    mtl = get_mention_ids_from_twitter()
    mdb = get_mentions_from_db()
    for m in mtl:
        if m not in mdb:
            mention = get_info(m)
            if mention['sender_id'] != me:
                try:
                    #Reply to mention:
                    api.update_status(f"Thanks for the mention, @{mention['sender_sn']}. I'm just a bot, so check out my creator @jheeeeezy! Follow us! - {id_generator()}", mention['mention_id'])
                    api.create_favorite(mention['mention_id'])
                    api.retweet(mention['mention_id'])
                    print(f"Retweeted and favorited {mention['mention_id']}")
                    add_to_db(mention['mention_id'])
                    if mention['sender_id'] not in people_i_follow:
                        try:
                            api.create_friendship(mention['sender_id'])
                            print(f"-> Just followed @{mention['sender_sn']}!")
                            short_wait()
                        except TweepError as error:
                            emsg = f"-> Error: #{id_generator()} @ {datetime.now()} => {error.reason}"
                            print(emsg)
                            send_error_email(emsg)
                            pass
                    short_wait()
                except TweepError as error:
                    emsg = f"-> Error: #{id_generator()} @ {datetime.now()} => {error.reason}"
                    print(emsg)
                    send_error_email(emsg)
                    pass
                except Exception as error:
                    emsg = f"-> Error: #{id_generator()} @ {datetime.now()} => {error}"
                    print(emsg)
                    send_error_email(emsg)
                    pass
                    
    print('** Done Replying to Mentions **')

            
# ---------------------------------------------------------------------------- #
if __name__ == "__main__":
    retweet_favorite_follow()