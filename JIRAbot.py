#!/usr/bin/python

import os
from slackclient import SlackClient
import time
import re
import requests

# Use environment variables for portability
api_token = os.environ['SLACK_EXPANDER_API_TOKEN'] # Required. If not set, will result in a KeyError
channel = os.environ['SLACK_EXPANDER_CHANNEL'] # Required. If not set, will result in a KeyError
jira_base_url = os.environ['JIRA_BASE_URL'] # Required. If not set, will result in a KeyError
bot_regex_raw = os.environ['SLACK_EXPANDER_BOT_REGEX'] # Required. If not set, will result in a KeyError
bot_icon_url = os.environ.get('SLACK_EXPANDER_BOT_ICON') # Optional. Not setting will result in bot having default picture
bot_username = 'JIRA Expander' # Change if you want your bot to post under a different name

sc = SlackClient(api_token)
msgs = []
bot_regex = re.compile(bot_regex_raw)

hist = sc.api_call('channels.history', channel=channel, count=1)['messages']
last = float(hist[0]['ts']) # timestamp of the latest message in the thread
while True:
 try:
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
 except requests.exceptions.ConnectionError as err:
  print 'Caught ConnectionError: Error ' + str(err.args[0].reason.errno) + ': ' + err.args[0].reason.strerror
  print 'Trying again...'
 except Exception as err2:
  print 'Caught Error:' + str(err2)
  print 'Trying again...'
