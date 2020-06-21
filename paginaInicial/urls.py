from django.urls import path

from paginaInicial.views import login_request, events_list, oauth2redirect, create, update # logout

urlpatterns = [
    path('', login_request, name="login"),
    path('events_list/', events_list, name='events_list'),
    path('events_list/create/', create, name='create'),
    path('events_list/update/<int:id>', update, name='update'),
    path('callback/', oauth2redirect, name='oauth2redirect'),
    ## path('oauth2callback/', oauth2redirect, name='oauth2redirect'),
    #path('logout', logout, name='logout'),
]
