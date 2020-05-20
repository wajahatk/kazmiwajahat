from time import sleep
from .models import DM, db
from os import getenv, system
from tweepy import (
    API,
    TweepError,
    OAuthHandler,
)


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
def refresh_dm_db():
    #Create DB
    try:
        system('python bot/dms/models.py db init')
        sleep(2)
    except:
        pass
    #Migrate
    try:
        system('python bot/dms/models.py db migrate')
        sleep(2)
    except:
        pass
    #create table & db:
    db.create_all()
    #Get dm id's from Twitter:
    msg_id_list = [int(message.id) for message in api.list_direct_messages()]
    #Get dm id's that are in DB:
    dms = [dm.msg_id for dm in DM.query.all()]
    
    print(f"DM_ID_LIST_BEFORE: {dms}")
    print(f"•••• Adding dm ids to the db: ••••")
    #Compare DMs to DMs in DB
    for msg_id in msg_id_list:
        #If DM not in DB:
        if msg_id not in dms:
            new_dm = DM(msg_id=msg_id)
            db.session.add(new_dm)
            db.session.commit()
    
    dms = [dm.msg_id for dm in DM.query.all()]
    print(f"•••• Done adding dm ids to the db: ••••")
    print(f"DM_ID_LIST_AFTER: {dms}")
    


# ---------------------------------------------------------------------------- #
if __name__ == "__main__":
    refresh_dm_db()