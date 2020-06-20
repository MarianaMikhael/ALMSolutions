import os
import json
#import pickle
import logging
import httplib2

#from datetime import datetime
from django.contrib.auth import authenticate, login#, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import (
    HttpResponse, HttpResponseBadRequest, HttpResponseRedirect)
#from googleapiclient.discovery import build
from oauth2client.contrib import xsrfutil
from oauth2client import client, file
from decouple import config

from apiclient.discovery import build
import pickle
#from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import datetime


class GoogleCalendar:

    SCOPES = [
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile',
        'https://www.googleapis.com/auth/calendar',
        ]

    def get_flow(request):
        flow = client.OAuth2WebServerFlow(
            client_id=config('google_client_id'),
            client_secret=config('google_client_secret'),
            redirect_uri='http://127.0.0.1:8000/callback',
            scope=SCOPES,
            access_type='offline',
            state=''
            )

        return flow


    def sent_to_API(title, start_time1, end_time1):
        # credentials = pickle.load(open("token.pkl", "rb"))
        # service = build("calendar", "v3", credentials=credentials)
        """"Get Credentials"""
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                    'calendar-python-quickstart.json')
        
        store = file.Storage(credential_path)
        credentials = store.get()        
        if not credentials or credentials.invalid is True:
            flow = get_flow(request)
            flow.params['state'] = xsrfutil.generate_token(config('SECRET_KEY'),
                                                        request.user)
            request.session['flow'] = pickle.dumps(flow).decode('iso-8859-1')
            authorize_url = flow.step1_get_authorize_url()
        
            return HttpResponseRedirect(authorize_url)

        service = build("calendar", "v3", credentials=credentials)

        """"Get my calendar"""
        result = service.calendarList().list().execute()
        calendar_id = result['items'][0]['id']

        """ Create a new event"""
        start_time1 = datetime.strptime(start_time1, "%Y-%m-%d %H:%M:%S")  # convert to datetime
        end_time1 = datetime.strptime(end_time1, "%Y-%m-%d %H:%M:%S")  # convert to datetime
        timezone = 'America/Sao_Paulo'

        event = {
            'summary': title,
            'location': 'ValeVerde',
            'description': 'Teste',
            'start': {
                'dateTime': start_time1.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': timezone,
            },
            'end': {
                'dateTime': end_time1.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': timezone,
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }
        service.events().insert(calendarId=calendar_id, body=event).execute()


    def edit_to_API(title, start_time1, end_time1, event_id):
        # credentials = pickle.load(open("token.pkl", "rb"))
        # service = build("calendar", "v3", credentials=credentials)
        # result = service.calendarList().list().execute()
        # calendar_id = result['items'][0]['id']
        # timezone = 'Europe/Warsaw'
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                    'calendar-python-quickstart.json')
        
        store = file.Storage(credential_path)
        credentials = store.get()        
        if not credentials or credentials.invalid is True:
            flow = get_flow(request)
            flow.params['state'] = xsrfutil.generate_token(config('SECRET_KEY'),
                                                        request.user)
            request.session['flow'] = pickle.dumps(flow).decode('iso-8859-1')
            authorize_url = flow.step1_get_authorize_url()
        
            return HttpResponseRedirect(authorize_url)

        service = build("calendar", "v3", credentials=credentials)    
        result = service.calendarList().list().execute()
        calendar_id = result['items'][0]['id']
        timezone = 'America/Sao_Paulo'
        
        event = {
            'summary': title,
            'location': 'ValeVerde',
            'description': 'Teste',
            'start': {
                'dateTime': start_time1.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': timezone,
            },
            'end': {
                'dateTime': end_time1.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': timezone,
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }
        service.events().update(calendarId=calendar_id, eventId=event_id, body=event).execute()


    def get_event_id():
        """ This function return google calendar event id as string - last value from table"""
        # credentials = pickle.load(open("token.pkl", "rb"))
        # service = build("calendar", "v3", credentials=credentials)
        # result = service.calendarList().list().execute()
        # calendar_id = result['items'][0]['id']
        # result = service.events().list(calendarId=calendar_id, maxResults=2400).execute()
        # table_size = len(result['items'])
        # event_id = result['items'][table_size - 1]['id']
        # return event_id
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                    'calendar-python-quickstart.json')
        
        store = file.Storage(credential_path)
        credentials = store.get()        
        if not credentials or credentials.invalid is True:
            flow = get_flow(request)
            flow.params['state'] = xsrfutil.generate_token(config('SECRET_KEY'),
                                                        request.user)
            request.session['flow'] = pickle.dumps(flow).decode('iso-8859-1')
            authorize_url = flow.step1_get_authorize_url()
        
            return HttpResponseRedirect(authorize_url)

        service = build("calendar", "v3", credentials=credentials)    
        result = service.calendarList().list().execute()
        calendar_id = result['items'][0]['id']
        result = service.events().list(calendarId=calendar_id, maxResults=2400).execute()
        table_size = len(result['items'])
        event_id = result['items'][table_size - 1]['id']
        return event_id


    def delete_from_API(event_id):
        # credentials = pickle.load(open("token.pkl", "rb"))
        # service = build("calendar", "v3", credentials=credentials)
        # result = service.calendarList().list().execute()
        # calendar_id = result['items'][0]['id']
        # service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                    'calendar-python-quickstart.json')
        
        store = file.Storage(credential_path)
        credentials = store.get()        
        if not credentials or credentials.invalid is True:
            flow = get_flow(request)
            flow.params['state'] = xsrfutil.generate_token(config('SECRET_KEY'),
                                                        request.user)
            request.session['flow'] = pickle.dumps(flow).decode('iso-8859-1')
            authorize_url = flow.step1_get_authorize_url()
        
            return HttpResponseRedirect(authorize_url)
        
        service = build("calendar", "v3", credentials=credentials)
        result = service.calendarList().list().execute()
        calendar_id = result['items'][0]['id']
        service.events().delete(calendarId=calendar_id, eventId=event_id).execute()


# ------------------------------------------------->

def oauth2redirect(request):
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    if not xsrfutil.validate_token(config('SECRET_KEY'),
                                   request.GET.get('state').encode('utf8'),
                                   request.user):

        return HttpResponseBadRequest()

    code = request.GET.get('code')
    error = request.GET.get('error')

    if code:
        flow = get_flow(request)
        credentials = flow.step2_exchange(code)
        storage = file.Storage(credential_path)
        storage.put(credentials)
        #request.session['creds'] = credentials.to_json()

        return HttpResponseRedirect('/')
    elif code is None and error:
        return HttpResponse(str(error))
    else:
        return HttpResponseBadRequest()

# ------------------------------------------------->
