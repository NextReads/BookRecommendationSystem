from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib import messages


import requests

# Create your views here.


# Create your views here.
def UserProfile(request):
    return render(request, "userprofile/userhome.html", {})

class UserRecommendations(View):
    def get(self, request):
        userToken = request.session.get('token')
        print("offffffff ",userToken)
        #headers = {'x-auth-token': userToken}
        #recommendationsResponse = requests.get('https://nextreadsbackend.azurewebsites.net/api/recommendations', headers=headers)
        #if recommendationsResponse.status_code == 200:
            #recommendations = recommendationsResponse.json()
        recommendations = [
                    {
                        "id": 1,
                        "title": "The Hunger Games",
                        "author": "Suzanne Collins",
                        "image": "https://images.gr-assets.com/books/1447303603m/2767052.jpg",
                        "rating": 4.33,
                        "description": "Could you survive on your own, in the wild, with everyone out to make sure you don't live to see the morning?"
                    },
                    {
                        "id": 2,
                        "title": "Harry Potter and the Philosopher's Stone",
                        "author": "J.K. Rowling",
                        "image": "https://images.gr-assets.com/books/1474154022m/3.jpg",
                        "rating": 4.44,
                        "description": "Harry Potter's life is miserable. His parents are dead and he's stuck with his heartless relatives, who force him to live in a tiny closet under the stairs."
                    },
                    
                ]
        return render(request, "userprofile/recommendations.html", {'recommendations': recommendations})
        #else:
            # return render(request, "userprofile/recommendations.html", {'recommendations': []})

class UserBooks(View):
    def get(self,request):
        try:
            userToken = request.session.get('token')
            headers = {'x-auth-token': userToken}
            booksResponse = requests.get('http://localhost:80/api/users/readbooks', headers=headers)
            print(booksResponse.status_code)
            if booksResponse.status_code == 201:
                books = booksResponse.json()
                print(books)
                return render(request, "userprofile/userbooks.html", {'books': books})
            else:
                print("error occured")
                return render(request, "userprofile/userbooks.html", {'books': []})
        except:
            messages.error(request, "error occured")
            return render(request, "userprofile/userbooks.html", {'books': []})
            

class tbrBooks(View):
    def get(self,request):
        try:
            userToken = request.session.get('token')
            headers = {'x-auth-token': userToken}
            booksResponse = requests.get('http://localhost:80/api/users/wanttoread', headers=headers)
            if booksResponse.status_code == 201:
                books = booksResponse.json()
                
                return render(request, "userprofile/tbrbooks.html", {'books': books})
            else:
                print("error occured")
                return render(request, "userprofile/tbrbooks.html", {'books': []})
        except:
            messages.error(request, "error occured")
            return render(request, "userprofile/tbrbooks.html", {'books': []})

class browseBooks(View):
    def get(self,request):
        return render(request, "userprofile/browseBooks.html",{} )