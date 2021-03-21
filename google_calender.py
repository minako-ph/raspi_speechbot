# -*- coding: utf-8 -*-
from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_events():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
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
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.now()
    today_start = str(now.year) + '-' + str(now.month).zfill(2) + '-' + str(now.day).zfill(2) + 'T00:00:00+09:00'
    today_end = str(now.year) + '-' + str(now.month).zfill(2) + '-' + str(now.day).zfill(2) + 'T23:59:59+09:00'

    events_result = service.events().list(calendarId='primary',
                                        timeMin=today_start,
                                        timeMax=today_end,
                                        maxResults=10,
                                        singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    event_text = ''

    if not events:
        event_text += u'今のところ特になし'
        print(event_text)
        return event_text
    else:
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            event_text += str(start[11:13]) + u'時' + str(start[14:16]) + u'分に'
            event_text += event['summary'] + u'、'
        print(event_text)
        return event_text

if __name__ == '__main__':
    get_events()
