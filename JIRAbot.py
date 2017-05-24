#!/usr/bin/python

import os
from slackclient import SlackClient
import time
import re

# Use environment variables for portability
api_token = os.environ['SLACK_EXPANDER_API_TOKEN']
channel = os.environ['SLACK_EXPANDER_CHANNEL']
jira_base_url = os.environ['JIRA_BASE_URL']
bot_regex_raw = os.environ['SLACK_EXPANDER_BOT_REGEX']
bot_icon_url = os.environ['SLACK_EXPANDER_BOT_ICON']
bot_username = 'JIRA Expander'

sc = SlackClient(api_token)
msgs = []
bot_regex = re.compile(bot_regex_raw)

hist = sc.api_call('channels.history', channel=channel, count=1)['messages']
last = float(hist[0]['ts']) # timestamp of the latest message in the thread
while True:
 links = []
 msgs = filter(lambda a: a is not None, map(lambda x: x if 'bot_id' not in x else None, hist)) # should only get non-bot responses
 msgs = filter(lambda b: b is not None, filter(lambda a: a if float(a['ts']) >= last else None, msgs)) # should filter out old messages, if they exist
 if not msgs:
  time.sleep(1)
  hist = sc.api_call('channels.history', channel=channel)['messages'] # Above logic will strip out old and bot messages
  continue # if there are no new messages, wait 1 second and then go again
 
 for msg in msgs: # the check above guarantees at msgs is not empty
  matches = bot_regex.findall(msg['text']) # Find all matches in the message
  for match in matches:
    links.append(jira_base_url + match) # Build a list of URLs based on the matches

 for link in links:
  last = float(sc.api_call('chat.postMessage', channel=channel, text=link, username=bot_username, as_user=False, icon_url=bot_icon_url)['ts']) # Post links to the channel and update last

 time.sleep(1) # Give time for new messages to hit channel
 hist = sc.api_call('channels.history', channel=channel)['messages'] # Get new messages
