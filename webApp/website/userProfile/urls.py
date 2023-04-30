from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
from .views import UserProfile, UserRecommendations, UserBooks, tbrBooks, browseBooks
app_name = 'userProfile'
urlpatterns = [
    path('recommendations', views.UserRecommendations, name='userrecommendations'),
    path('userhome', views.UserProfile, name='userhome'),
    path('userbooks', views.UserBooks, name='userbooks'),
    path('tbrbooks', views.tbrBooks, name='tbrbooks'),
    path('browsebooks',views.browseBooks, name='browseBooks')
]