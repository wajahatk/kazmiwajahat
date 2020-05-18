from time import sleep
from os import getenv, system
from bot.mailer import send_error_email
from subprocess import Popen, PIPE
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, g, make_response
from tweepy import Cursor, TweepError, API, OAuthHandler
from bot.waits import short_wait, med_wait, long_wait
from bot import (
    models,
    pick_status,
    follow_back,
    retweet_hashtags,
    get_my_followers,
    create_auth_json,
    delete_old_tweets,
    get_people_i_follow,
    unfollow_nonfollowers,
    retweet_favorite_follow,
    find_trending_topics_in_usa,
    find_new_friends_based_on_trend_list,
) 


# ----------------------------------- Flask ---------------------------------- #
app = Flask(__name__)


# --------------------------------- DB Config -------------------------------- #
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
db = SQLAlchemy(app)
host = getenv('HOST')
port = getenv('PORT')

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
auth = OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)
# API Variable:
api = API(auth, wait_on_rate_limit=True)


# ---------------------------------------------------------------------------- #
class TwitterBot:
    #Create auth.json for twitter-to-sqlite
    def set_up_ttsql():
        try:
            create_auth_json.create_auth_json()
        except Exception as error:
            print(f"-> ERROR @ 'set_up_ttsql': {error}")
            try:
                send_error_email.send_error_email(error)
            except Exception as error:
                print(f"-> ERROR @ 'set_up_ttsql'.'send_error_email': {error}")
                pass
            pass

    #Delete old tweets:
    def remove_old_tweets_from_timeline():
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print("Picking a status from the list...")
        try:
            delete_old_tweets.delete_old_tweets()
        except Exception as error:
            print(f"-> ERROR @ 'remove_old_tweets_from_timeline': {error}")
            try:
                send_error_email.send_error_email(error)
            except Exception as error:
                print(f"-> ERROR @ 'remove_old_tweets_from_timeline'.'send_error_email': {error}")
                pass
            pass
        print(f"** Done deleting tweets... **")
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")

    #Update status from list:
    def post_status():
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        try:
            status = pick_status.pick_status()
            api.update_status(status)
            print("-> Status posted!!!")
        except Exception as error:
            print(f"-> ERROR @ 'post_status': {error}")
            try:
                send_error_email.send_error_email(error)
            except Exception as error:
                print(f"-> ERROR @ 'post_status'.'send_error_email': {error}")
                pass
            pass
        print("** Done with Status... **")
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    
    #Retweet hashtags from list:
    #Follow users from on search based on same list:
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
        try:
            retweet_hashtags.retweet_hashtags(hashtags)
            find_new_friends_based_on_trend_list.find_new_friends_based_on_trend_list(hashtags)
        except Exception as error:
            print(f"-> ERROR @ 'retweet_my_hashtags': {error}")
            try:
                send_error_email.send_error_email(error)
            except Exception as error:
                print(f"-> ERROR @ 'retweet_my_hashtags'.'send_error_email': {error}")
                pass
            pass
        print("** Done Retweeting... **")
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")

    #Reply to mentions, favorite those, and follow user:
    def reply_to_mentions_and_follow():
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print("Replying to user's that have mentioned me and following them!")
        # Set all tweets that mention my user to list:
        try:
            mentions = api.mentions_timeline(tweet_mode='extended')
            following = get_people_i_follow.get_people_i_follow()
            retweet_favorite_follow.retweet_favorite_follow(mentions, following)
        except Exception as error:
            print("-> ERROR @ 'reply_to_mentions_and_follow'")
            try:
                send_error_email.send_error_email(error)
            except Exception as error:
                print(f"-> ERROR @ 'reply_to_mentions_and_follow'.'send_error_email': {error}")
                pass
            pass
        print("** Done with mentions... **")
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")

    #Follow users back:
    def follow_back():
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print("Giving my followers the ol' follow back...")
        try:
            me = api.me().screen_name
            followers = get_my_followers.get_my_followers()
            following = get_people_i_follow.get_people_i_follow()
            follow_back.follow_back(followers, following)
        except Exception as error:
            print(f"-> ERROR @ 'follow_back': {error}")
            try:
                send_error_email.send_error_email(error)
            except Exception as error:
                print(f"-> ERROR @ 'follow_back'.'send_error_email': {error}")
                pass
            pass
        print("** Done with 'Follow Back' **")
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        
    #Unfollow people that don't follow bot:
    def unfollow_nonfollowers():
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print("Unfollowing those that don't me...")
        try:
            me = api.me().screen_name
            followers = get_my_followers.get_my_followers()
            following = get_people_i_follow.get_people_i_follow()
            unfollow_nonfollowers.unfollow_nonfollowers(followers, following)
        except Exception as error:
            print(f"-> ERROR @ 'unfollow_nonfollowers': {error}")
            try:
                send_error_email.send_error_email(error)
            except Exception as error:
                print(f"-> ERROR @ 'unfollow_nonfollowers'.'send_error_email': {error}")
                pass
            pass
        print("** Done unfollowing... **")
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")

    #Find and retweet trending hashtags:
    def retweet_trending_topics():
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print("Now, I'm searching for trending topics in the USA for posts to retweet...")
        try:
            usa_trends = find_trending_topics_in_usa.find_trending_topics_in_usa()
            retweet_hashtags,retweet_hashtags(usa_trends)
        except Exception as error:
            print(f"-> ERROR @ 'retweet_trending_topics: {error}")
            try:
                send_error_email.send_error_email(error)
            except Exception as error:
                print(f"-> ERROR @ 'retweet_trending_topics'.'send_error_email': {error}")
                pass
            pass
        print("** Done Retweeting... **")
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")

    #Find users to follow based on hashtag list:
    def follow_trendy_users():
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print("** Following trendy users: **")
        try:
            trends = find_trending_topics_in_usa.find_trending_topics_in_usa()
            find_new_friends_based_on_trend_list.find_new_friends_based_on_trend_list(trends)
        except Exception as error:
            print(f"-> ERROR @ 'follow_trendy_users: {error}")
            try:
                send_error_email.send_error_email(error)
            except Exception as error:
                print(f"-> ERROR @ 'follow_trendy_users'.'send_error_email': {error}")
                pass
            pass
        print("** Done Following trendy users... **")
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    
    #Use twitter-to-sqlite to refresh dbs:
    def refresh_db():
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print('Updating user-timeline & mentions DBs... This may take a few mins...')
        try:
            system('twitter-to-sqlite user-timeline twitter.db')
            system('twitter-to-sqlite mentions-timeline twitter.db')
        except Exception as error:
            print(f"-> ERROR @ 'refresh_db: {error}")
            try:
                send_error_email.send_error_email(error)
            except Exception as error:
                print(f"-> ERROR @ 'refresh_db'.'send_error_email': {error}")
                pass
            pass
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")


# ---------------------------------- Run Bot --------------------------------- #
if __name__ == "__main__":
    print('|-|-|Configuring twitter-to-sqlite...|-|-|')
    TwitterBot.set_up_ttsql()
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
        med_wait.med_wait()
        TwitterBot.retweet_my_hashtags()
        print('(┛ಠ_ಠ)┛彡┻━┻')
        print("////-------Medium Rest Period-------////")
        med_wait.med_wait()
        TwitterBot.follow_back()
        TwitterBot.post_status()
        print('┳━┳ ヽ(ಠل͜ಠ)ﾉ')
        print("////-------Medium Rest Period-------////")
        med_wait.med_wait()
        TwitterBot.retweet_trending_topics()
        print('(╯°Д°)╯︵/(.□ . \)')
        print("////-------Medium Rest Period-------////")
        med_wait.med_wait() 
        TwitterBot.follow_trendy_users()
        TwitterBot.post_status()
        print('(˚Õ˚)ر ~~~~╚╩╩╝')
        print("////-------Medium Rest Period-------////")
        short_wait.short_wait()
        TwitterBot.unfollow_nonfollowers()
        print('┏━┓┏━┓┏━┓ ︵ /(^.^/)')
        print("////-------Medium Rest Period-------////")
        short_wait.short_wait()
        TwitterBot.reply_to_mentions_and_follow()
        print('┻━┻︵ \(°□°)/ ︵ ┻━┻')
        print("////-------Medium Rest Period-------////")
        med_wait.med_wait()
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print("Getting ready to start again!")
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print('┏━┓┏━┓┏━┓ ︵ /(^.^/)')
        print("////-------Long Rest Period-------////")
        long_wait.long_wait()
        