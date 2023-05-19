from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        if not labels:
            print('No labels found.')
        else:
            print('Labels:')
            for label in labels:
                print(label['name'])

    except Exception as error:
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    main()

from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import email
import base64 #add Base64
import time 

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

        #Filter and get the IDs of the message I need. 
        #I'm just filtering messages that have the label "UNREAD"

    try:
        service = build('gmail', 'v1', credentials=creds)
        search_id = service.users().messages().list(userId='me', labelIds="UNREAD").execute()
        number_result = search_id['resultSizeEstimate']

        final_list = [] # empty array, all the messages ID will be listed here

        # review if the search is empty or not
        # if it has messages on it, It will enter the for

        if number_result>0:
            message_ids = search_id['messages']

            for ids in message_ids:
                final_list.append(ids['id'])
                # call the function that will call the body of the message
                get_message(service, ids['id'] )

            return final_list

        # If there are not messages with those criterias 
        #The message 'There were 0 results for that search string' will be printed. 

        else:
            print('There were 0 results for that search string')
            return ""

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')

        #new function to get the body of the message, and decode the message

def get_message(service, msg_id):

    try:
        message_list=service.users().messages().get(userId='me', id=msg_id, format='raw').execute()

        msg_raw = base64.urlsafe_b64decode(message_list['raw'].encode('ASCII'))

        msg_str = email.message_from_bytes(msg_raw)

        content_types = msg_str.get_content_maintype()

        #how it will work when is a multipart or plain text

        if content_types == 'multipart':
            part1, part2 = msg_str.get_payload()
            print("This is the message body, html:")
            print(part1.get_payload())
            return part1.get_payload()
        else:
            print("This is the message body plain text:")
            print(msg_str.get_payload())
            return msg_str.get_payload()

    except HttpError as error:
        #This script authenticates the user, reads the unread emails, and prints their contents. Please replace `"UNREAD"` with the label you're using for the newsletters if it's different. Note that this script assumes that the emails are either in plain text or multipart/alternative with HTML and plain text parts. If the emails have a different structure, you may need to modify this script to correctly extract the content.

The next step would be to process and summarize the content of the newsletters. This is where the OpenAI API would come into play. You could use the OpenAI GPT-3 model to generate summaries of the newsletters. 

Here is a basic example of how you might use the OpenAI API to generate a summary:

```python
import openai

openai.api_key = 'your-api-key'

response = openai.Completion.create(
  engine="text-davinci-002",
  prompt="Summarize: " + newsletter_content,
  temperature=0.3,
  max_tokens=100
)

print(response.choices[0].text.strip())

import discord

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

    channel = client.get_channel(your_channel_id)
    await channel.send(summary)

client.run('your-bot-token')
