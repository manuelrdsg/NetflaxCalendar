import tweepy, json, dropbox
from array import array
from dropbox.files import WriteMode
import httplib2
import os
import credentials

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'

consumer_key = credentials.consumer_key
consumer_secret = credentials.consumer_secret
access_token = credentials.google_access_token
access_token_secret = credentials.google_access_token_secret

token = credentials.dropbox_token
dbx = dropbox.Dropbox(token)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
    return credentials

##-------------------------------------------------------------------------------------------------

credentials = get_credentials()
http = credentials.authorize(httplib2.Http())
service = discovery.build('calendar', 'v3', http=http)

path = "/netflax.json"
file_temp = "downloads/netflax.json"
dbx.files_download_to_file(file_temp, path)

with open(file_temp,"r") as f:
    data = f.read()

d = json.loads(data)

# Now, separate info from the tweet which has just been tweeted
num_of_elements = len(d)
id = num_of_elements

events = service.events().list(calendarId='primary').execute()

lista = events.get('items', [])

summary = []
for i in range(len(lista)):
    summary.append(lista[i]["summary"])

print("Añadido: ")
for i in range(1,len(d)+1):
    event = {
        'summary': d[str(i)]["Name"],
        'start': {
            'date': d[str(i)]["Year"] + "-" + d[str(i)]["Month"] + "-" + d[str(i)]["Day"],
        },
        'end': {
            'date': d[str(i)]["Year"] + "-" + d[str(i)]["Month"] + "-" + d[str(i)]["Day"],
        },
    }

    if event['summary'] not in summary:
        print(event['summary']+",")
        event = service.events().insert(calendarId='primary', body=event).execute()
