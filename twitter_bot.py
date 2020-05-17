import tweepy
from time import sleep
from logic.logic import Logic
from os import getenv, environ
import sqlite3
from flask import Flask, g, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import json
from models import Tweets
from subprocess import Popen, PIPE
# ----------------------------------- Flask ---------------------------------- #
app = Flask(__name__)

# --------------------------------- DB Config -------------------------------- #
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
db = SQLAlchemy(app)
host = getenv('HOST')
port = environ.get('PORT')

# -------------------------------- Twitter API ------------------------------- #
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
auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)
# API Variable:
api = tweepy.API(auth, wait_on_rate_limit=True)

# ---------------------------------------------------------------------------- #
class TwitterBot:
    def __init__(self, username, password):
        self.username = userna

    def create_auth_json():
        #Create auth.json file for twitter-to-sqlite
        p = Popen(['twitter-to-sqlite', 'auth'], stdin=PIPE)
        p.stdin.write(f"{api_key}\n".encode())
        p.stdin.write(f"{api_secret}\n".encode())
        p.stdin.write(f"{access_token}\n".encode())
        p.stdin.write(f"{access_token_secret}\n".encode())
        p.stdin.flush()
        return

    def post_status():
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Picking a status from the list...")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        try:
            status = Logic.pick_status()
            api.update_status(status)
            print("-> Status posted!!!")
        except tweepy.TweepError as error:
            print("-> Couldn't update your status this time around.")
            print(f"-> Error: {error.reason}")
            pass
        print("**Done with Status...**")

    def retweet_my_hashtags():
        hashtags = [
            '#webdevelopment', 
            '#memes', 
            '#skateboarding', 
            '#thrasher', 
            '#hiphop', 
            '#coding', 
            '#100daysofcode',
            '#gamedev',
            '#jordan',
            '#NikeSB',
            '#crypto',
            '#ufc',
            '#videogames',
            '#newmusic',
            '#WashingtonDC',
            '#dcrestaurant'
        ]
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Now, I'm searching for hashtag posts to retweet...")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        Logic.retweet_hashtags(hashtags)
        print("**Done Retweeting...**")

    def reply_to_mentions_and_follow():
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Replying to user's that have mentioned me and following them!")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        # Set all tweets that mention my user to list:
        mentions = api.mentions_timeline(tweet_mode='extended')
        following = Logic.get_people_i_follow()
        Logic.retweet_favorite_follow(mentions, following)
        print("**Done with mentions...**")

    def follow_back():
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Giving my followers the ol' follow back...")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        me = api.me().screen_name
        followers = Logic.get_my_followers()
        following = Logic.get_people_i_follow()
        Logic.follow_back(followers, following)
        print("**Done with 'Follow Back'**")
        
    def unfollow_nonfollowers():
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Unfollowing those that have unfollowed me...")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        me = api.me().screen_name
        followers = Logic.get_my_followers()
        following = Logic.get_people_i_follow()
        Logic.unfollow_nonfollowers(followers, following)
        print("**Done unfollowing...**")
    
    def refresh_db():
        Logic.refresh_usertimeline_db()


# ---------------------------------- Run Bot --------------------------------- #
if __name__ == "__main__":
    print('|-|-|Configuring twitter-to-sqlite...|-|-|')
    TwitterBot.create_auth_json()
    sleep(30)
    while True:
        print("Twitter Bot Started!")
        print('Updating User-Timeline DB... This may take a few mins...')
        print('(╯°□°)╯︵ ┻━┻')
        TwitterBot.refresh_db()
        TwitterBot.post_status()
        print('┬─┬ノ( º _ ºノ)')
        print("////-------Med Rest Period-------////")
        Logic.med_wait()
        TwitterBot.retweet_my_hashtags()
        print('┳━┳ ヽ(ಠل͜ಠ)ﾉ')
        print("////-------Medium Rest Period-------////")
        Logic.med_wait()
        TwitterBot.follow_back()
        print('(┛ಠ_ಠ)┛彡┻━┻')
        print("////-------Medium Rest Period-------////")
        Logic.med_wait()
        TwitterBot.unfollow_nonfollowers()
        print('┏━┓┏━┓┏━┓ ︵ /(^.^/)')
        print("////-------Medium Rest Period-------////")
        Logic.med_wait()
        TwitterBot.reply_to_mentions_and_follow()
        print('┻━┻︵ \(°□°)/ ︵ ┻━┻')
        print("////-------Medium Rest Period-------////")
        Logic.med_wait()
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Getting ready to start again!")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print('(˚Õ˚)ر ~~~~╚╩╩╝')
        print("////-------Long Rest Period-------////")
        Logic.long_wait()
        