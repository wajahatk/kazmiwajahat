import tweepy
from time import sleep
from random import choice, shuffle
from os import getenv, system
from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from smtplib import SMTP, SMTPException
from ssl import create_default_context
from datetime import datetime, timedelta
from models import MentionsTweets

# ------------------------------------- - ------------------------------------ #
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

# ------------------------------------- - ------------------------------------ #
class BotLogic:
    # ----------------------------------- Waits ---------------------------------- #
    def short_wait(): #0.5 mins - 1 min
        #Set list of nums for random sleep time:
        sleep_nums = [num for num in range(30, 61)]
        #Return a random sleep time:
        return sleep(choice(sleep_nums))

    def med_wait(): #1 mins - 10 mins
        #Set list of nums for random sleep time:
        sleep_nums = [num for num in range(60, 601)]
        #Return a random sleep time:
        return sleep(choice(sleep_nums))

    def long_wait(): #10 min - 60 mins
        #Set list of nums for random sleep time:
        sleep_nums = [num for num in range(600, 3600)]
        #Return a random sleep time:
        return sleep(choice(sleep_nums))

    # ------------------------------ User-type Logic ----------------------------- #
    def delete_old_tweets():
        days_to_keep = 5
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        tweets_to_save = []
        print("¨…¨…¨Retrieving timeline tweets¨…¨…¨")
        timeline = tweepy.Cursor(api.user_timeline).items()
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
            except tweepy.TweepError as error:
                print("-> Couldn't update your status this time around.")
                BotLogic.send_error_email(error)
                print(f"-> Error: {error.reason}")
        print(f"¨…¨…¨Deleted {deletion_count} tweets from user-timeline¨…¨…¨")
        print(f"         ¨…¨…¨Ignored {ignored_count} tweets¨…¨…¨")
        
    def pick_status():
        status_options = [
            "If you were a triangle youd be acute one.",
            "eBay is so useless. I tried to look up lighters and all they had was 13,749 matches.",
            "(┛ಠ_ಠ)┛彡┻━┻",
            "Check out my creator's portfolio here: https://jharriswebdev.herokuapp.com/ #freelance #webdeveloper #coding #100DaysOfCode",
            "My creator is kind of funny, too. Check him out: @jheeeeezy #bot",
            "@jheeeeezy is the one that created me! Check him out!",
            "Beep boop boop bmmmmmmmmm *~*laser sounds*~* beep",
            "Best bot in the biz, baby! #bot #webdev #coding #python",
            "*- Does robot dance to future music -*",
            "Share a meme with me!",
            "@jheeeeezy .... --- .--     -- .- -. -.--     .--. . --- .--. .-.. .     .- .-. .     --. --- .. -. --.     - ---     - .-. .- -. ... .-.. .- - .     - .... .. ...     .--- ..- ... -     - ---     ..-. .. -. -..     .. - ...     .--- ..- ... -     - .... .. ...     --.- ..- . ... - .. --- -. ··--··",
            "これは英語ではありません！",
            "@jheeeeezy can create a bot for you, too! #bot #freelance #hitmeup #work",
            "https://jharriswebdev.herokuapp.com/ #freelance #webdev",
        ]
        return choice(status_options)

    def retweet_hashtags(hashtag_list):
        shuffle(hashtag_list)
        for hashtag in hashtag_list:
            tweetNumber = 2
            tweets = tweepy.Cursor(api.search, hashtag).items(tweetNumber)
            for tweet in tweets:
                try:
                    tweet.retweet()
                    print("-> Retweet Done!")
                    BotLogic.short_wait()
                except tweepy.TweepError as error:
                    print(error.reason)
                    BotLogic.send_error_email(error)
                    pass
                BotLogic.med_wait()

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
                    BotLogic.short_wait()
                except tweepy.TweepError as error:
                    print(f"-> Error: {error.reason}")
                    BotLogic.send_error_email(error)
                    pass
                except AttributeError as att_error:
                    print(f"‹‹‹‹ Attribute Error => {att_err} ››››")
                    BotLogic.send_error_email(att_error)
                    pass
            if mention.user.id not in people_i_follow:
                try:
                    api.create_friendship(mention.user.screen_name)
                    print(f"-> Just followed @{mention.user.screen_name}!")
                    BotLogic.short_wait()
                except tweepy.TweepError as error:
                    print(f"-> Error: {error.reason}")
                    BotLogic.send_error_email(error)
                    pass
            BotLogic.short_wait()
        #Update mentions in database:
        system('twitter-to-sqlite mentions-timeline twitter.db')
        print("Updated mentions db...")

    def refresh_usertimeline_db():
        system('twitter-to-sqlite user-timeline twitter.db')
        system('twitter-to-sqlite mentions-timeline twitter.db')

    def find_trending_topics_in_usa():
        trending_topic_list = []
        trends_available = api.trends_available()
        try:
            usa = api.trends_place(23424977)  #USA = 23424977
            for trend_list in usa:
                for (k,v) in trend_list.items():
                    for event in v:
                        if isinstance(event, dict):
                            for (a, b) in event.items():
                                if a == 'name':
                                    trending_topic_list.append(b)
            return trending_topic_list
        except tweepy.TweepError as error:
            print(f"-> Error: {error.reason}")
            BotLogic.send_error_email(error)
            pass

    # ------------------------------ Follower Logic ------------------------------ #
    def follow_back(followers, people_i_follow):
        for person in followers:
            if person not in people_i_follow:
                try:
                    api.create_friendship(person)
                    user = api.get_user(person)
                    print(f"-> Just followed @{user.screen_name}!")
                    BotLogic.med_wait()
                except tweepy.TweepError as error:
                    print(f"-> Error: {error.reason}")
                    BotLogic.send_error_email(error)
                    pass
            elif person in people_i_follow:
                user = api.get_user(person)
                print(f"-> You already follow @{user.screen_name}.")

    def unfollow_nonfollowers(followers, people_i_follow):
        for person in people_i_follow:
            if person not in followers:
                try:
                    user = api.get_user(person)
                    print(f"-> {user.screen_name} not in followers")
                    api.destroy_friendship(person)
                    print(f"-> Unfollowed @{user.screen_name}...")
                except tweepy.TweepError as error:
                    print(f"-> Error: {error.reason}")
                    BotLogic.send_error_email(error)
                    pass

    def get_people_i_follow():
        try:
            following = api.friends()
        except tweepy.TweepError as error:
            print(f"-> Error: {error.reason}")
            BotLogic.send_error_email(error)
            pass
        following_id_list = []
        try:
            for page in tweepy.Cursor(api.friends_ids).pages():
                following_id_list.extend(page)
            return following_id_list
        except tweepy.TweepError as error:
            print(f"-> Error: {error.reason}")
            BotLogic.send_error_email(error)
            pass

    def get_my_followers():
        try:
            followers = api.followers()
        except tweepy.TweepError as error:
            print(f"-> Error: {error.reason}")
            BotLogic.send_error_email(error)
            pass
        follower_id_list = []
        try:
            for page in tweepy.Cursor(api.followers_ids).pages():
                follower_id_list.extend(page)
                sleep(10)
            return follower_id_list
        except tweepy.TweepError as error:
            print(f"-> Error: {error.reason}")
            BotLogic.send_error_email(error)
            pass
        
    def find_users_to_follow_based_on_trend_list(trend_list):
        tweet_number = 1
        trends = trend_list
        for trend in trends:
            try:
                tweets = tweepy.Cursor(api.search, trend).items(tweet_number)
                for tweet in tweets:
                    try:
                        api.create_friendship(tweet.user.id)
                        print(f'-> Followed @{tweet.user.screen_name}!')
                        BotLogic.med_wait()
                    except tweepy.TweepError as error:
                        BotLogic.send_error_email(error)
                        print(f"-> ERROR: {error.reason}")
                        pass
            except tweepy.TweepError as error:
                print(f"-> Error: {error.reason}")
                BotLogic.send_error_email(error)
                pass 
            BotLogic.short_wait()

    # ------------------------------- Mailer Logic ------------------------------- #
    def send_error_email(error_to_send):
        smtp_server = "smtp.gmail.com"
        port = 587 # For starttls
        sender = getenv('SENDER_EMAIL')
        receiver = getenv('REC_EMAIL')
        pw = getenv('SENDER_PW')
        msg = f"""\
        Subject: JoshBot9000 Error

        Error: {error_to_send}
        """
        context = create_default_context()
        try:
            server = SMTP(smtp_server, port)
            server.starttls(context=context)
            server.login(sender, pw)
            server.sendmail(sender, receiver, msg)         
            print(f"…÷÷÷ Sent error email to {sender} ÷÷÷…")
        except SMTPException:
            print("Error: unable to send email")
        finally:
            server.quit()