## Dependencies
This app requires SlackClient to work. SlackClient is maintained by the Slack Developer Tools team, and of this writing it can be found at https://pypi.python.org/pypi/slackclient. It can also be easily installed if you have pip installed, by doing `pip install slackclient`

SlackClient is the only dependency of this project. However, some Endpoint Security programs (looking at you, Kaspersky) will require you to add the bot to a trusted list, or all API requests will automatically be blocked.

## Description

This is a simple Slack bot written in Python designed to monitor messages sent to a single channel and act on them. This bot was primarily designed to allow a user to reference a ticket number in plaintext (i.e. TICKET-1234), and have a bot automatically chat a link to the associated ticket.

The bot checks the given channel once per second for new messages that were not posted by a bot. It then runs the new messages through a Regular Expression, and matches to the RegEx are acted upon.

This app DOES NOT REQUIRE OAuth authentication as designed, although if the code is modified to try and use a more advanced feature of the Slack API (such as creating a user group or unfurling a link), it will require more extensive modification to authenticate over OAuth

## Setup
For portability, all settings are stored in environment variables except for the username, which is hardcoded to 'JIRA Expander'. To change this, just change the assignment of the bot_username variable in JIRAbot.py

A list of required environment variables and their purpose is as follows

# SLACK_EXPANDER_API_TOKEN: The API token allowing your bot to read and post messages to a channel. To find this token, navigate to <your Slack Domain>/apps/manage, and click the Custom Integrations tab. Click on 'Bots', and then 'Add Configuration'. When the configuration has been added, you will see an API token has been generated. Slack API tokens begin with the string 'xoxb-'

# SLACK_EXPANDER_CHANNEL: The id of the channel the bot will monitor and post to. Note this is not a plaintext channel such as #channel. To get a list of channels, do the following from a python interactive shell. (you must have your SLACK_EXPANDER_API_TOKEN environment variable set for this to work)

```
import os
from slackclient import SlackClient
sc = SlackClient(os.environ['SLACK_EXPANDER_API_TOKEN']
map(lambda x: (x['name'], x['id']), sc.api_call('channels.list')['channels'])
```

This will result in a list of 2-tuples of the form (<channel_name>, <channel_id>) to print. Pick the ID of the channel you're interested in, and set that as your SLACK_EXPANDER_CHANNEL environment variable

# JIRA_BASE_URL
The base url of your JIRA domain. As an example, mine is `https://<company JIRA>/browse/PROJECT-`, and regex matches (see next section) will be appended to this URL

# SLACK_EXPANDER_BOT_REGEX
The Regular Expression you want your bot to use to find ticket names and numbers to link to. The app uses re.findall to get the matches, so no worries about capturing repeating groups here. As an example, mine is set to 'PROJECT-([0123456789]{4,}), which will match anything that begins with the string 'PROJECT-' and is followed by four or more numbers

# SLACK_EXPANDER_BOT_ICON
A URL containing an image file for your bot to use. If this is unset it's not the end of the world, you'll just have the Slack default bot icon set for your bot. I highly recommend using the image found at http://cultofthepartyparrot.com/parrots/hd/gentlemanparrot.gif

## Usage
To use the bot, just ensure that the relevant environment variables are set and run ./JIRAbot.py from whereever you installed this package. It can run in the background just fine.

I have no interest in continuing to support this project. If it doesn't work for you, sorry. I made it because I couldn't find a free bot online that does exactly this (listens to a channel and posts messages based on their content), and after I made it I thought others might find it useful. Please don't contact me asking how something works or why something is broken - it should be easy to install, easy to use, and easy to modify for your own purposes if you so choose to do so.

Happy Botting!
