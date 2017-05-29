import tweepy, json, dropbox
from dropbox.files import WriteMode
#from __future__ import print_function
import httplib2
import os
import credentials

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from server import update
import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'

token = credentials.dropbox_token
dbx = dropbox.Dropbox(token)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):

        tweet = status.text
        tweet_formatted = ""
        i = 0

        date = ""
        name = ""

        while(tweet[i] != '\n'):
            tweet_formatted += tweet[i]
            i += 1

        tweet_formatted = tweet_formatted.split()

        date = tweet_formatted[0]
        name = ' '.join(tweet_formatted[1:(len(tweet_formatted) - 1)])

        # Get info from date string
        dateSplitted = date.split('/')

        day = dateSplitted[0]
        month = dateSplitted[1]
        year = "20" + dateSplitted[2]

        if int(day) < 10:
            day = "0" + day

        if int(month) < 10:
            month = "0" + month

        update.delay(day, month, year, name)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

myStream.filter(follow=["4891680879"], async=True)
