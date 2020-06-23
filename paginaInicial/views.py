import os
import json
import pickle
import logging
import httplib2

from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import (
    HttpResponse, HttpResponseBadRequest, HttpResponseRedirect)
from googleapiclient.discovery import build
from oauth2client.contrib import xsrfutil
from oauth2client import client, file
from decouple import config

from paginaInicial.models.post_events import Post
from paginaInicial.forms.login_form import UserLogin
from paginaInicial.forms.post_events_form import PostForm

logger = logging.getLogger(__name__)

# -------------------------------------------------> Login ALMSolutions

# ALMSolutions Login Page and Redirect to Google Authentication
def login_request(request):
    context = {}
    form = UserLogin(request.POST or None)
    if request.POST:
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            #login(request, user)
            return redirect('events_list')
    
    context['form'] = form
    return render(request, 'paginaInicial/login.html', context)


# -------------------------------------------------> Login Google oAuth 2.0

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


def events_list(request):
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                'calendar-python-quickstart.json')
    
    store = file.Storage(credential_path)
    credentials = store.get()
    logger.error(credentials)
    
    if not credentials or credentials.invalid is True:
        flow = get_flow(request)
        flow.params['state'] = xsrfutil.generate_token(config('SECRET_KEY'),
                                                       request.user)
        request.session['flow'] = pickle.dumps(flow).decode('iso-8859-1')
        authorize_url = flow.step1_get_authorize_url()
    
        return HttpResponseRedirect(authorize_url)

    service = build("calendar", "v3", credentials=credentials)

    now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print(now)
    events = service.events()
    event_list = events.list(
        calendarId='primary',
        timeMin=now,
        singleEvents=True,
        orderBy='startTime',
        ).execute()

    return render(request, 'paginaInicial/home.html', {'events': event_list})


# -------------------------------------------------> Create Event

def sent_to_API(request, summary, location, description, start_time1, end_time1, email):
    """Get Credentials"""
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

    """Get Calendar"""
    result = service.calendarList().list().execute()
    calendar_id = result['items'][0]['id']

    """Create a New Event"""
    eventStartDate = convertToRFC3339DatetimeFormat(start_time1)
    eventEndDate = convertToRFC3339DatetimeFormat(end_time1)
    timezone = 'Brazil/East'    

    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': eventStartDate,
            'timeZone': timezone,
        },
        'end': {
            'dateTime': eventEndDate,
            'timeZone': timezone,
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
        'attendees': [
            {'email': email},
        ],
    }
    service.events().insert(calendarId=calendar_id, sendNotifications=True, body=event).execute()


def create(request, template_name='paginaInicial/create_events_form.html'):
    """ Function which add new record to database and to google calendar"""
    form = PostForm(request.POST or None)
    if form.is_valid():
        summary = form.data['summary']
        location = form.data['location']
        description = form.data['description']
        start_time1 = form.data['start']
        end_time1 = form.data['end']
        email = form.data['email']
        
        sent_to_API(request, summary, location, description, start_time1, end_time1, email)

        """ assign event id to uidd filed"""
        replace = form.save(commit=False)
        replace.uidd = get_event_id(request)
        replace.save()
        form.save()
        return redirect('events_list')

    return render(request, template_name, {'form': form})


# -------------------------------------------------> Edit Event

def edit_to_API(request, summary, location, description, start_time1, end_time1, email, uidd):
    """This function return google calendar event id as string - last value from table"""
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
    timezone = 'Brazil/East'

    eventStartDate = convertToRFC3339DatetimeFormat(start_time1)
    eventEndDate = convertToRFC3339DatetimeFormat(end_time1)

    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': eventStartDate,
            'timeZone': timezone,
        },
        'end': {
            'dateTime': eventEndDate,
            'timeZone': timezone,
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
        'attendees': [
            {'email': email},
        ],
    }
    service.events().update(calendarId=calendar_id, sendNotifications=True, eventId=uidd, body=event).execute()


def update(request, uidd, template_name='paginaInicial/update_events_form.html'):
    # calendar = get_object_or_404(Post, pk=pk)
    # form = PostForm(request.POST or None, instance=calendar)
    form = PostForm(request.POST or None)
    if form.is_valid():
        summary = form.data['summary']
        location = form.data['location']
        description = form.data['description']
        start_time = form.data['start']
        end_time = form.data['end']
        email = form.data['email']
        uidd = form.data['uidd']

        start_time1 = convertToBrazilianDatetimeFormat(start_time)
        end_time1 = convertToBrazilianDatetimeFormat(end_time)
 
        edit_to_API(request, summary, location, description, start_time1, end_time1, email, uidd)
        form.save()

        return redirect('events_list')
    
    return render(request, template_name, {'form': form, 'uidd' : uidd})


# -------------------------------------------------> Delete Event

def delete_from_API(request, uidd):
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
    service.events().delete(calendarId=calendar_id, sendNotifications=True, eventId=uidd).execute()


def delete(request, uidd, template_name='paginaInicial/delete_events_form.html'):
    # my_event = get_object_or_404(Post, pk=pk)
    form = PostForm(request.POST or None)
    if request.method == 'POST':
        delete_from_API(request, uidd)
        # my_event.delete()
        return redirect('events_list')
    
    return render(request, template_name, {'form': form, 'uidd': uidd})


# -------------------------------------------------> Utils

# Make sure that the request is from who we think it is
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

        return HttpResponseRedirect('/events_list')
    elif code is None and error:
        return HttpResponse(str(error))
    else:
        return HttpResponseBadRequest()


def get_event_id(request):
    """ This function return google calendar event id as string - last value from table"""
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
    uidd = result['items'][table_size - 1]['id']
    
    return uidd


def convertToRFC3339DatetimeFormat(brazilianDateTime):
    year =   brazilianDateTime[6:10]
    month =  brazilianDateTime[3:5]
    day =    brazilianDateTime[0:2]
    hour =   brazilianDateTime[11:13]
    minute = brazilianDateTime[14:16]
    second = brazilianDateTime[17:19]

    return f'{year}-{month}-{day}T{hour}:{minute}:{second}'


def convertToBrazilianDatetimeFormat(isoFormatDateTime):
    year =   isoFormatDateTime[0:4]
    month =  isoFormatDateTime[5:7]
    day =    isoFormatDateTime[8:10]
    hour =   isoFormatDateTime[11:13]
    minute = isoFormatDateTime[14:16]
    second = isoFormatDateTime[17:19]

    return f'{day}-{month}-{year} {hour}:{minute}:{second}'


# -------------------------------------------------> Logout ALMSolutions

# ALMSolutions Logout and Delete Delete Credentials oAuth 2.0

@login_required
def logout(request):
    user = request.user
    credentials = CredentialsModel.objects.get(id=user.id)
    credentials.revoke(httplib2.Http())
    credentials.delete()
    storage = DjangoORMStorage(CredentialsModel, 'id', user, 'credential')
    storage.delete()

    auth_logout(request)
    return HttpResponseRedirect('/')
