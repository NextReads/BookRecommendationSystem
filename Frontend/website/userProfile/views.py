from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib import messages
from django.http import JsonResponse



import requests

# Create your views here.


# Create your views here.
def UserProfile(request):
    # get to read next book
    def getToReadNext():
        userToken = request.session.get('token')
        headers = {'x-auth-token': userToken}
        toReadNextResponse = requests.get('http://localhost:80/api/users/toreadnext', headers=headers)
        if toReadNextResponse.status_code == 200:
            toReadNext = toReadNextResponse.json()
            #change bookId[_id] to bookId[id]
            toReadNext['id'] = toReadNext.pop('_id')
            return toReadNext
        else:
            return JsonResponse({'message_error': 'error in getting to read next book.'}, status=400)
        
    return render(request, "userprofile/userhome.html", {'toReadNext': getToReadNext()})

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
            if booksResponse.status_code == 201:
                books = booksResponse.json()
                #book has bookId which includes all the details of the book
                #rename bookId[_id] to bookId[id]

                for book in books:
                    book['bookId']['id'] = book['bookId'].pop('_id')

                return render(request, "userprofile/userbooks.html", {'books': books})
            else:
                print("error occured")
                return render(request, "userprofile/userbooks.html", {'books': []})
        except:
            print(request, "error occured")
            return render(request, "userprofile/userbooks.html", {'books': []})
            

class tbrBooks(View):
    def get(self,request):
        try:
            userToken = request.session.get('token')
            headers = {'x-auth-token': userToken}
            booksResponse = requests.get('http://localhost:80/api/users/wanttoread', headers=headers)
            if booksResponse.status_code == 201:
                books = booksResponse.json()
                for book in books:
                    book['id'] = book.pop('_id')
                return render(request, "userprofile/tbrbooks.html", {'books': books})
            else:
                print("error occured")
                return render(request, "userprofile/tbrbooks.html", {'books': []})
        except:
            print(request, "error occured")
            return render(request, "userprofile/tbrbooks.html", {'books': []})
    
class rateBook(View):
    def post(self,request):
        bookId = request.POST.get('fe_eh')
        rating = request.POST.get('rating')
        print("bookId zsfsdgds ",bookId)
        print("rating ",rating)
        try:
            userToken = request.session.get('token')
            headers = {'x-auth-token': userToken}
            data = {'bookId': bookId, 'rating': rating}
            response = requests.post('http://localhost:80/api/books/'+ str(bookId)+'/rating', json=data, headers=headers)
            if response.status_code == 201:
                messages.success(request, 'Book rated successfully')
                return redirect('userProfile:userbooks')
            else:
                messages.error(request, 'Error occured while rating book')
                return redirect('userProfile:userbooks')
        except:
            messages.error(request, 'Error occured while rating book')
            return redirect('userProfile:userbooks')
        
class reviewBook(View):
    def post(self,request):
        bookId = request.POST.get('bookIdentifier')
        review = request.POST.get('reviewText')
        print("bookId",bookId)
        print("review",review)

        try:
            userToken = request.session.get('token')
            headers = {'x-auth-token': userToken}
            data = {'review': review}
            response = requests.post('http://localhost:80/api/books/'+ str(bookId)+'/review', json=data, headers=headers)
            if response.status_code == 201:
                return redirect('userProfile:userbooks')
            else:
                print(response.status_code, response.text)
                return redirect('userProfile:userbooks')
        except:
            return redirect('userProfile:userbooks')
        
class setToReadNext(View):
    def post(self,request):
        bookId = request.POST.get('book_id')
        print("bookId",bookId)
        try:
            userToken = request.session.get('token')
            headers = {'x-auth-token': userToken}
            response = requests.post('http://localhost:80/api/users/'+ str(bookId) +'/toreadnext', headers=headers)
            if response.status_code == 201:
                messages.success(request, 'set to read next successfully')
                return redirect('userProfile:tbrbooks')
            else:
                messages.error(request,response.text)
                return redirect('userProfile:tbrbooks')
        except:
            messages.error(request, response.text)
            return redirect('userProfile:tbrbooks')
        
class browseBooks(View):
    def get(self,request):
        return render(request, "userprofile/browseBooks.html",{} )
    
## bookDetails as function
def bookDetails(request, book_id):
    #print("bookId",book_id)
    try:
        response = requests.get('http://localhost:80/api/books/book/'+ str(book_id))
        if response.status_code == 200:
            book = response.json()
            print(book)
            return render(request, "bookDetails.html", {'book': book})
        else:
            messages.error(request, response.text)
            return redirect('userProfile:userbooks')
        
    except: 
        return redirect('userProfile:userbooks')
    
#645aa639dfa36522587195d2