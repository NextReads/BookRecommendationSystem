from django.urls import path
from . import views
from .views import SignupView, LoginView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('signup', SignupView.as_view(), name='signup'),
    path('validate-username', csrf_exempt(views.UsernamesValidationView.as_view()), name='validate-username'),
    path('validate-email', csrf_exempt(views.EmailValidationView.as_view()), name='validate-email'),
    path('set-goal-step', views.setGoalStepView.as_view(), name='set-goal-step'),
    path('rate-books-step', views.rateBooksStepView.as_view(), name='rate-books-step'),
    path('logout', views.logoutView.as_view(), name='logout'),
    path('rate-book', views.rateBook.as_view(), name='rate-book'),
    path('want-to-read', views.wantToRead.as_view(), name='want-to-read'),
    #####################
    path('search', views.searchBooks, name='search-books'),
    path('genre/<str:genre>', views.getGenre, name='get-genre'),


]