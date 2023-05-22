from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib import messages
from django.http import JsonResponse



import requests

# Create your views here.
def getToReadNext(request):
        try:
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
        except:
            return JsonResponse({'message_error': 'error in getting to read next book.'}, status=400)
        

# Create your views here.
def UserProfile(request):
    # get to read next book
    return render(request, "userprofile/userhome.html", {'toReadNext': getToReadNext(request)})

class UserRecommendations(View):
    def get(self, request):
        try:
            userToken = request.session.get('token')
            #print("offffffff ",userToken)
            headers = {'x-auth-token': userToken}
            recommendationsResponse = requests.get('http://localhost:80/api/books/recommend', headers=headers)
            if recommendationsResponse.status_code == 200:
                recommendations = recommendationsResponse.json()
                #print("recommendations ",recommendations)
                return render(request, "userprofile/recommendations.html", {'recommendations': recommendations})
            else:
                return render(request, "userprofile/recommendations.html", {'recommendations': []})
        except:
            return render(request, "userprofile/recommendations.html", {'recommendations': []})
        # recommendations = [
        #             {
        #                 "id": 1,
        #                 "title": "The Hunger Games",
        #                 "author": "Suzanne Collins",
        #                 "image": "https://images.gr-assets.com/books/1447303603m/2767052.jpg",
        #                 "rating": 4.33,
        #                 "description": "Could you survive on your own, in the wild, with everyone out to make sure you don't live to see the morning?"
        #             },
        #             {
        #                 "id": 2,
        #                 "title": "Harry Potter and the Philosopher's Stone",
        #                 "author": "J.K. Rowling",
        #                 "image": "https://images.gr-assets.com/books/1474154022m/3.jpg",
        #                 "rating": 4.44,
        #                 "description": "Harry Potter's life is miserable. His parents are dead and he's stuck with his heartless relatives, who force him to live in a tiny closet under the stairs."
        #             },
                    
        #         ]

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
                messages.error(request, 'Error occured while rating book1')
                return redirect('userProfile:userbooks')
        except:
            messages.error(request, 'Error occured while rating book2')
            return redirect('userProfile:userbooks')
        
class reviewBook(View):
    def post(self,request):
        bookId = request.POST.get('bookIdentifier')
        review = request.POST.get('reviewText')
        #print("bookId",bookId)
        #print("review",review)

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
        #let page = request.GET.get('page')
        page = 5
        try:
            response = requests.get('http://localhost:80/api/books/getbooks?page='+str(page))
            if response.status_code == 200:
                books = response.json()
                return render(request, "userprofile/browseBooks.html", {'books': books})
            else:
                print(response.status_code, response.text)
                return render(request, "userprofile/browseBooks.html", {'books': []})
        except:
            print(response.status_code, response.text)
            return render(request, "userprofile/browseBooks.html", {'books': []})
##################################
def similarBooks(genre):
        try:
            response = requests.get('http://localhost:80/api/books/genre/', params={'pageNumber': 1, 'genre': genre})
            if response.status_code == 200:
                books = response.json()
                return books
            else:
                return None
        except: 
            return None
def getAllGenreBooks():
    try:
        page = 5
        response =  requests.get('http://localhost:80/api/books/getbooks?page='+str(page))
        if response.status_code == 200:
            books = response.json()
            return books
        else:
            return None
    except: 
        return None  
    
def addToWantToRead(request, book_id):
    try:
        userToken = request.session.get('token')
        headers = {'x-auth-token': userToken}
        response = requests.post('http://localhost:80/api/users/'+ str(book_id)+'/wantToRead', headers=headers)
        print("response ",response.text)
        if response.status_code == 201:
            return {'message_success': response.text}
        else:
            return {'message_error': response.text}
    except:
        return None
        
#################################         
def bookDetails(request, book_id):
    print("bookId",book_id)
    def getbookdetails(book_id):
        try:
            response = requests.get('http://localhost:80/api/books/book/'+ str(book_id))
            if response.status_code == 200:
                book = response.json()
                return book
            else:
                return None
        except: 
            return None
           
    book = getbookdetails(book_id)
    genres = book['genres'].split(',')
    genre = genres[0]
    # split the description to 2 parts to display in the book details page
    #first part is the first 3 sentences
    #second part is the rest of the description
    description = book['description'].split('.')
    if len(description) > 3:
        book['description1'] = description[0] + '.' + description[1] + '.' + description[2] + '.'
        book['description2'] = '.'.join(description[3:]) + '.'
    else:
        book['description1'] = book['description']
        book['description2'] = ''
    book['id'] = book.pop('_id')
    #print("book ",book)
    
    similarbooks = similarBooks(genre)
    #print("similarbooks ",similarbooks['books'])    
    #convert bookId[_id] to bookId[id]
    for x in similarbooks['books']:
        x['id'] = x.pop('_id')

    if book:
        return render(request, "bookDetails.html", {'book': book, 'similarbooks': similarbooks['books']})
    else:
        messages.error(request, 'Error occured while getting book details')
        return redirect('userProfile:userbooks')
    
def getGenre(request,genre):
    if(genre == 'all'):
        books = getAllGenreBooks()
        for x in books:
            x['id'] = x.pop('_id')
        return render(request, "userprofile/browseBooks.html", {'books': books})
    else:
        #print("genre ",genre)
        books = similarBooks(genre)
        for x in books['books']:
            x['id'] = x.pop('_id')
        if books:
            return render(request, "userprofile/browseBooks.html", {'books': books['books']})
        else:
            messages.error(request, 'Error occured while getting books')
            return render(request, "userprofile/browseBooks.html", {'books': []})

def wantToReadBrowse(request):
    book_id = request.POST.get('book_id')

    response = addToWantToRead(request, book_id)
    #print("response ",response)
    if response:
        if 'message_success' in response:
            messages.success(request, response['message_success'])
            return redirect('userProfile:get-genre', genre='all')
        else:
            messages.error(request, response['message_error'])
            return redirect('userProfile:get-genre', genre='all')
    else:
        messages.error(request, 'Error occured while adding book to want to read')
        return redirect('userProfile:get-genre', genre='all')
    
def searchBooks(request):
    search = request.POST.get('query')
    print("search ",search)
    try:

        response = requests.get("http://localhost:80/api/books/search/", params={'pageNumber': 1, 'search': search})
        if response.status_code == 200:
            books = response.json()
            
            for x in books['books']:
                x['id'] = x.pop('_id')
            messages.success(request, 'Search results for ' + search)
            return render(request, "userprofile/browseBooks.html", {'books': books['books']})
        
                                
        else:
                messages.error(request, response.text)
                return render(request, "userprofile/browseBooks.html", {'books': []})
            
    except:
        return render(request, "userprofile/browseBooks.html", {'books': []})
        
        
    
def searchInRead(request):
    search = request.POST.get('query')
    print("search ",search)
    try:
        userToken = request.session.get('token')
        headers = {'x-auth-token': userToken}
        response = requests.get('http://localhost:80/api/users/searchinread', params={'pageNumber': 1, 'search': search}, headers=headers)
        if response.status_code == 200:
            books = response.json()
            print("books ",books)
            for x in books:
                x['bookId']['id'] = x['bookId'].pop('_id')
            messages.success(request, 'Search results for ' + search)
            return render(request, "userprofile/userbooks.html", {'books': books})
        else:
            messages.error(request, 'Error occured while searching for books')
            return render(request, "userprofile/userbooks.html", {'books': []})
    except:
        return render(request, "userprofile/userbooks.html", {'books': []})
    
def searchInTbr(request):
    search = request.POST.get('query')
    print("search ",search)
    try:
        userToken = request.session.get('token')
        headers = {'x-auth-token': userToken}
        response = requests.get('http://localhost:80/api/users/searchintbr', params={'pageNumber': 1, 'search': search}, headers=headers)
        if response.status_code == 200:
            books = response.json()
            print("books ",books)
            for x in books:
                x['id'] = x.pop('_id')
            messages.success(request, 'Search results for ' + search)
            return render(request, "userprofile/tbrbooks.html", {'books': books})
        else:
            messages.error(request, 'Error occured while searching for books')
            return render(request, "userprofile/tbrbooks.html", {'books': []})
    except:
        return render(request, "userprofile/tbrbooks.html", {'books': []})