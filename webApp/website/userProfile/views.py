from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.


# Create your views here.
def UserProfile(request):
    return render(request, "userprofile/userhome.html", {})

def UserRecommendations(request):
    return render(request, "userprofile/recommendations.html", {})

def UserBooks(request):
    return render(request, "userprofile/userbooks.html", {})

def tbrBooks(request):
    return render(request, "userprofile/tbrBooks.html",{} )

def browseBooks(request):
    return render(request, "userprofile/browseBooks.html",{} )