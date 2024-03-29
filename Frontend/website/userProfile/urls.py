from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
from .views import UserProfile, UserRecommendations, UserBooks, tbrBooks, rateBook
app_name = 'userProfile'
urlpatterns = [
    path('recommendations', views.UserRecommendations.as_view(), name='userrecommendations'),
    path('recommendationsPage', views.recommendationsPage.as_view(), name='userrecommendationspage'),
    path('userhome', views.UserProfile, name='userhome'),
    path('userbooks', views.UserBooks.as_view(), name='userbooks'),
    path('tbrbooks', views.tbrBooks.as_view(), name='tbrbooks'),
    #path('browsebooks',views.browseBooks.as_view(), name='browseBooks'),
    path('userbooks/ratebook', views.rateBook.as_view(), name='ratebook'),
    path('userbooks/reviewbook', views.reviewBook.as_view(), name='reviewbook'),
    path('userhome/to-read-next', views.setToReadNext.as_view(), name='to-read-next'),
    path('book/<str:book_id>', views.bookDetails, name='book-details'),
    path('browseBooks/genre/<str:genre>/<int:pageNumber>', views.getGenre, name='get-genre'),
    path('browseBooks/want-to-read-browse', views.wantToReadBrowse, name='want-to-read-browse'),
    path('book/want-to-read/<str:book_id>', views.wantToReadBookDetails, name='want-to-read-book-details'),
    path('search', views.searchBooks, name='search-books'),
    path('searchinread', views.searchInRead, name='search-in-read'),
    path('searchintbr', views.searchInTbr, name='search-in-tbr'),
    path('setreadinggoal', views.setReadingGoal, name='set-reading-goal'),
    path('deletetbr/<str:book_id>',views.deleteFromTbr, name='delete-tbr'),
    path('deleteread/<str:book_id>/<int:rating>',views.deleteFromRead, name='delete-read'),
    path('setcurrentbook/<str:book_id>',views.setCurrentBook, name='set-current-book'),

]