# josh_bot_9000
An automated Twitter bot, created with Python 3 and Tweepy. Hosted on Heroku, running 24/7. Auto reply, like and favorite when mentioned. Auto-retweet specified hashtags. Posts status updates. Follows the users that follow the bot. Unfollows those not found in followers list. Messages coming soon 

To host your own on Heroku:

-> Get your Keys and Tokens from https://developer.twitter.com/apps

-> Create an app on Heroku

-> Set the keys and tokens from Twitter as follows in your .env and in the Environment settings on Heroku:
```
CONSUMER_KEY=<Consumer API Key goes here>
CONSUMER_SECRET=<Consumer API Secret goes Here>
API_KEY=<Access token goes here>
API_SECRET=<Access token secret goes here>
SQLALCHEMY_DATABASE_URI=<sqlite:///twitter.db>
SQLALCHEMY_TRACK_MODIFICATIONS=False
```
-> Connect Heroku to Github in the deployment section and setup auto builds.

-> Watch the logs to see your bots progress and watch it flip tables!

In order to keep the bot running and avoid the free dynos provided from heroku from idling, register you app at http://kaffeine.herokuapp.com/
