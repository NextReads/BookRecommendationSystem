from django.shortcuts import render

# Create your views here.
from django.shortcuts import render


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