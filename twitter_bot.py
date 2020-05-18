import tweepy
from time import sleep
from bot.bot import BotLogic
from os import getenv, environ
from flask import Flask, g, make_response
from flask_sqlalchemy import SQLAlchemy
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
    def create_auth_json():
        #Create auth.json file for twitter-to-sqlite
        p = Popen(['twitter-to-sqlite', 'auth'], stdin=PIPE)
        p.stdin.write(f"{api_key}\n".encode())
        p.stdin.write(f"{api_secret}\n".encode())
        p.stdin.write(f"{access_token}\n".encode())
        p.stdin.write(f"{access_token_secret}\n".encode())
        p.stdin.flush()
        return

    def remove_old_tweets_from_timeline():
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print("Picking a status from the list...")
        BotLogic.delete_old_tweets()
        print(f"≤≤≤ Done deleting tweets ≥≥≥")
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")

    def post_status():
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        try:
            status = BotLogic.pick_status()
            api.update_status(status)
            print("-> Status posted!!!")
        except tweepy.TweepError as error:
            print("-> Couldn't update your status this time around.")
            BotLogic.send_error_email(error)
            print(f"-> Error: {error.reason}")
            pass
        print("**Done with Status...**")
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    
    def retweet_my_hashtags():
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
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print("Now, I'm searching for hashtag posts to retweet...")
        BotLogic.retweet_hashtags(hashtags)
        BotLogic.find_users_to_follow_based_on_trend_list(hashtags)
        print("**Done Retweeting...**")
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")

    def reply_to_mentions_and_follow():
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print("Replying to user's that have mentioned me and following them!")
        # Set all tweets that mention my user to list:
        mentions = api.mentions_timeline(tweet_mode='extended')
        following = BotLogic.get_people_i_follow()
        BotLogic.retweet_favorite_follow(mentions, following)
        print("**Done with mentions...**")
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")

    def follow_back():
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print("Giving my followers the ol' follow back...")
        me = api.me().screen_name
        followers = BotLogic.get_my_followers()
        following = BotLogic.get_people_i_follow()
        BotLogic.follow_back(followers, following)
        print("**Done with 'Follow Back'**")
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        
    def unfollow_nonfollowers():
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print("Unfollowing those that don't me...")
        me = api.me().screen_name
        followers = BotLogic.get_my_followers()
        following = BotLogic.get_people_i_follow()
        BotLogic.unfollow_nonfollowers(followers, following)
        print("**Done unfollowing...**")
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")

    def retweet_trending_topics():
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print("Now, I'm searching for trending topics in the USA for posts to retweet...")
        usa_trends = BotLogic.find_trending_topics_in_usa()
        BotLogic.retweet_hashtags(usa_trends)
        print("**Done Retweeting...**")
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")

    def follow_trendy_users():
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print("** Following trendy users: **")
        trends = BotLogic.find_trending_topics_in_usa()
        BotLogic.find_users_to_follow_based_on_trend_list(trends)
        print("** Done Following trendy users... **")
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    
    def refresh_db():
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print('Updating user-timeline & mentions DBs... This may take a few mins...')
        BotLogic.refresh_usertimeline_db()
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")


# ---------------------------------- Run Bot --------------------------------- #
if __name__ == "__main__":
    print('|-|-|Configuring twitter-to-sqlite...|-|-|')
    TwitterBot.create_auth_json()
    sleep(10)
    while True:
        print("Twitter Bot Started!")
        print('┬─┬ノ( º _ ºノ)')
        TwitterBot.remove_old_tweets_from_timeline()
        print('(╯°□°)╯︵ ┻━┻')
        TwitterBot.refresh_db()
        TwitterBot.post_status()
        print('┬─┬ノ( ಠ ل͜ಠノ)')
        print("////-------Med Rest Period-------////")
        BotLogic.med_wait()
        TwitterBot.retweet_my_hashtags()
        print('(┛ಠ_ಠ)┛彡┻━┻')
        print("////-------Medium Rest Period-------////")
        BotLogic.med_wait()
        TwitterBot.follow_back()
        TwitterBot.post_status()
        print('┳━┳ ヽ(ಠل͜ಠ)ﾉ')
        print("////-------Medium Rest Period-------////")
        BotLogic.med_wait()
        TwitterBot.retweet_trending_topics()
        print('(╯°Д°)╯︵/(.□ . \)')
        print("////-------Medium Rest Period-------////")
        BotLogic.med_wait() 
        TwitterBot.follow_trendy_users()
        TwitterBot.post_status()
        print('(˚Õ˚)ر ~~~~╚╩╩╝')
        print("////-------Medium Rest Period-------////")
        BotLogic.short_wait()
        TwitterBot.unfollow_nonfollowers()
        print('┏━┓┏━┓┏━┓ ︵ /(^.^/)')
        print("////-------Medium Rest Period-------////")
        BotLogic.short_wait()
        TwitterBot.reply_to_mentions_and_follow()
        print('┻━┻︵ \(°□°)/ ︵ ┻━┻')
        print("////-------Medium Rest Period-------////")
        BotLogic.med_wait()
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print("Getting ready to start again!")
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print('┏━┓┏━┓┏━┓ ︵ /(^.^/)')
        print("////-------Long Rest Period-------////")
        BotLogic.long_wait()
        