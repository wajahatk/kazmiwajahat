const { Autohook } = require('twitter-autohook');
const request = require('request');
const util = require('util');
const get = util.promisify(request.get);
const post = util.promisify(request.post);
require('dotenv').config();


/* -------------------------------------------------------------------------- */
function auto_reply_to_dms(){
(async start => {
  try {
    const webhook = new Autohook();
    //Wait on direct message events
    webhook.on('event', async event => {
        if (event.direct_message_events) {
            await sayHi(event);
        }
        async function sayHi(event) {
            //Check if DM:
            if (!event.direct_message_events) {
                return;
            }
            //Get first element from message array:
            const message = event.direct_message_events.shift()
            //Check if msg is valid:
            if (typeof message === 'undefined' || typeof message.message_create === 'undefined') {
                return;
            }
            if (message.message_create.sender_id === message.message_create.target.recipient_id) {
                return;
            }
            //Prepare and send teh msg reply:
            const senderScreenName = event.users[message.message_create.sender_id].screen_name;

            const oAuthConfig = {
                consumer_key: process.env.CONSUMER_KEY,
                consumer_secret: process.env.CONSUMER_SECRET,
                token: process.env.API_KEY,
                token_secret: process.env.API_SECRET,
            };

            const requestConfig = {
                url: "https://api.twitter.com/1.1/direct_messages/events/new.json",
                oauth: oAuthConfig,
                json: {
                    event: {
                        type: 'message_create',
                        message_create: {
                            target: {
                                recipient_id: message.message_create.sender_id,
                            },
                            message_data: {
                                text: `Hi @${senderScreenName}! 👋`
                            }
                        }
                    }
                }
            };
            await post(requestConfig);
        }
    });

    // Removes existing webhooks
    await webhook.removeWebhooks();
    // Starts a server and adds a new webhook
    await webhook.start();
    
    oauth_token = process.env.TWITTER_ACCESS_TOKEN
    oauth_token_secret = process.env.TWITTER_ACCESS_TOKEN_SECRET
    // Subscribes to your own user's activity
    await webhook.subscribe({oauth_token, oauth_token_secret});  
  } catch (e) {
    // Display the error and quit
    console.error(e);
    process.exit(1);
  }
})();
}
module.exports = {
    auto_reply_to_dms
}