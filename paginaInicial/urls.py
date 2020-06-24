from django.urls import path

from paginaInicial import views

urlpatterns = [
    path('', views.login_request, name="login"),
    path('logout/', views.logout_request, name='logout_request'),
    path('events_list/', views.events_list, name='events_list'),
    path('events_list/create/', views.create, name='create'),
    path('events_list/update/<str:uidd>', views.update, name='update'),
    path('events_list/delete/<str:uidd>', views.delete, name='delete'),
    path('callback/', views.oauth2redirect, name='oauth2redirect'),
    ## path('oauth2callback/', oauth2redirect, name='oauth2redirect'),
    #path('logout', logout, name='logout'),
]
