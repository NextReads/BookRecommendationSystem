from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
from .views import UserProfile, UserRecommendations, UserBooks, tbrBooks, browseBooks, rateBook
app_name = 'userProfile'
urlpatterns = [
    path('recommendations', views.UserRecommendations.as_view(), name='userrecommendations'),
    path('userhome', views.UserProfile, name='userhome'),
    path('userbooks', views.UserBooks.as_view(), name='userbooks'),
    path('tbrbooks', views.tbrBooks.as_view(), name='tbrbooks'),
    path('browsebooks',views.browseBooks.as_view(), name='browseBooks'),
    path('userbooks/ratebook', views.rateBook.as_view(), name='ratebook'),
    path('userbooks/reviewbook', views.reviewBook.as_view(), name='reviewbook'),
    path('userhome/to-read-next', views.setToReadNext.as_view(), name='to-read-next'),
    path('book/<str:book_id>', views.bookDetails, name='book-details'),

]