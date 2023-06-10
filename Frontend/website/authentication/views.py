from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from validate_email import validate_email
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import json
import requests
from requests.exceptions import RequestException



class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body) 
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid.'}, status=400)
        
        return JsonResponse({'email_valid': True})
           
    
# Create your views here.
class UsernamesValidationView(View):
    def post(self, request):
        data = json.loads(request.body) 
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Username should only contain alphanumeric characters.'}, status=400)
       
        return JsonResponse({'username_valid': True})

class SignupView(View):
    def get(self, request):
        return render(request, "authentication/signup.html", {})
    
    def post(self, request):
        # Get user data
        # validate data
        # redirect to login page
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confrimPassword = request.POST.get('confirmPassword')
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        print ("firstName", firstName)
        print ("lastName", lastName)
        role = "Member"
        context = {
            'fieldValues': request.POST
        }
        if len(password) < 8:
            messages.error(request, 'Password too short.')
            return render(request, "authentication/signup.html", context)
        if password != confrimPassword:
            messages.error(request, 'Passwords do not match.')
            return render(request, "authentication/signup.html", context)
        
        data={'username': username, 'email': email, 'password': password, 'firstName': firstName, 'lastName': lastName, 'role': role}
        try:
            response = requests.post('http://localhost:80/api/users', json=data)
            if response.status_code == 201:
                userToken = response.headers['x-auth-token']
                #save token in session
                request.session['token'] = userToken
                messages.success(request, response.text)
                return redirect('set-goal-step')
            else:
                messages.error(request, response.text)
                return render(request, "authentication/signup.html", {})
        except RequestException as e:
            messages.error(request, "An error occurred while making the request. Please try again later.")
            return render(request, "authentication/signup.html", {})


class LoginView(View):
    def get(self, request):
        return render(request, "authentication/login.html", {})
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        context = {
            'fieldValues': request.POST
        }
        if username and password:
            data={'username': username, 'password': password}
            try:
                response = requests.post('http://localhost:80/api/users/login', json=data)
                
                if response.status_code == 201:
                    userToken = response.headers['x-auth-token']
                    print("userToken", response.headers['x-auth-token'])
                    #save token in session
                    request.session['token'] = userToken
                    #messages.success(request, response.text)
                    return redirect('userProfile:userhome')
                else:
                    messages.error(request, response.text)
                    return render(request, "authentication/login.html", context)
            except RequestException as e:
                messages.error(request, "An error occurred while making the request. Please try again later.")
                return render(request, "authentication/login.html", context)
        else:
            messages.error(request, 'Please fill all fields.')
            return render(request, "authentication/login.html", context)

class logoutView(View):
    def post(self, request):
        #logout user
        if request.session.has_key('token'):
           print("token", request.session['token'])
           request.session.flush()

        #auth.logout(request)        
        messages.success(request, 'You have been logged out.')
        return redirect('login')
           
class setGoalStepView(View):
    def post(self, request):
        try:
            userToken = request.session.get('token')
            headers = {'x-auth-token': userToken}
            readingGoal = request.POST.get('user_challenge[goal]')
            data = {'readingGoal': readingGoal}
            print("data", data)
            response = requests.post('http://localhost:80/api/users/setreadinggoal', json=data, headers=headers)
            if response.status_code == 201:
                return redirect('rate-books-step')
            else:
                messages.error(request, response.text)
                return redirect('rate-books-step')
        except:
            messages.error(request, 'Error occured while setting reading goal')
            return redirect('rate-books-step')
        
    def get(self, request):
        return render(request, "authentication/set-goal-step.html", {})

class rateBooksStepView(View):
    def get(self, request):
            page = 10
            context = {}
            headers = {'x-auth-token':request.session['token'] }

            try:
                rateCount = requests.get('http://localhost:80/api/users/ratedbooks', headers=headers)
                if rateCount.status_code == 200:
                    rateCount = rateCount.json()
                    print("rateCount", rateCount)
                    request.session['rateCount'] = rateCount
            except RequestException as e:
                messages.error(request, "An error occurred while making the request. Please try again later.")
                return render(request, "authentication/rate-books-step.html", {})


            try:
                booksResposne = requests.get('http://localhost:80/api/books/getbooks?page='+str(page))
                print("booksResposne", booksResposne.status_code)
                if booksResposne.status_code == 200:
                    books = booksResposne.json()
                    #rename _id to id
                    for book in books:
                        book['id'] = book.pop('_id')

                    context = {
                        'books': books
                    }
                    if context:
                        return render(request, "authentication/rate-books-step.html", context)
                else:
                        messages.error(request, booksResposne.text)
                        return render(request, "authentication/rate-books-step.html", {})
            except:
                return render(request, "authentication/rate-books-step.html", {})

class rateBook(View):

    def post(self, request):
        bookId = request.POST.get('book_id')
        rating = request.POST.get('rating')
        print("bookId", bookId)
        print("rating", rating)
        headers = {'x-auth-token':request.session['token'] }
        print("headers", headers)

        # get number of rated books by user
        try:
            rateCount = requests.get('http://localhost:80/api/users/ratedbooks', headers=headers)
            if rateCount.status_code == 200:
                rateCount = rateCount.json()
                print("rateCount", rateCount)
                request.session['rateCount'] = rateCount
        except RequestException as e:
            print("An error occurred while making the request. Please try again later.")

        #rate book request
        if bookId and rating:
            data={'bookId': bookId, 'rating': rating}
            try:
                response = requests.post('http://localhost:80/api/books/'+ str(bookId)+'/rating', json=data, headers=headers)
                print("response", response.text)
                print("response", response.status_code)
                if response.status_code == 201:
                    messages.success(request, response.text)
                    return redirect('rate-books-step')

                else:
                    messages.error(request, response.text)
                    return redirect('rate-books-step')
            except RequestException as e:
                messages.error(request, "An error occurred while making the request. Please try again later.")
                return redirect('rate-books-step')

        else:
            messages.error(request, 'Please specify rating.')
            return redirect('rate-books-step')

class wantToRead(View):
    def post (self, request):
        bookId = request.POST.get('book_id')
        print("bookId", bookId)
        try:
            headers = {'x-auth-token':request.session['token'] }
            response = requests.post('http://localhost:80/api/users/'+ str(bookId)+'/wantToRead', headers=headers)
            print("response", response.text)
            print("response", response.status_code)
            if response.status_code == 201:
                messages.success(request, response.text)
                return redirect('rate-books-step')

            else:
                messages.error(request, response.text)
                return redirect('rate-books-step')
        except RequestException as e:
            messages.error(request, "An error occurred while making the request. Please try again later.")
            return redirect('rate-books-step')
        
def setReadingGoal(request):
    try:
        userToken = request.session.get('token')
        headers = {'x-auth-token': userToken}
        readingGoal = request.POST.get('user_challenge[goal]')
        data = {'readingGoal': readingGoal}
        response = requests.post('http://localhost:80/api/users/setreadinggoal', json=data, headers=headers)
        if response.status_code == 201:
            messages.success(request, 'Reading goal set successfully')
            return redirect('rate-books-step')
        else:
            messages.error(request, response.text)
            return redirect('rate-books-step')
    except:
        messages.error(request, 'Error occured while setting reading goal')
        return redirect('rate-books-step')
       
################################################################################
        
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
def getAllGenreBooks(pageNumber):
    try:
        response =  requests.get('http://localhost:80/api/books/getbooks?page='+str(pageNumber))
        if response.status_code == 200:
            books = response.json()
            return books
        else:
            return None
    except: 
        return None  

def getGenre(request,genre, pageNumber):
    if(genre == 'all'):
        books = getAllGenreBooks(pageNumber)
        if books:
            for x in books:
                x['id'] = x.pop('_id')
            return render(request, "authentication/rate-books-step.html", {'books': books})
        else:
            messages.error(request, 'Error occured while getting books')
            return render(request, "authentication/rate-books-step.html", {'books': []})
    else:
        books = similarBooks(genre)
        if books:
            for x in books['books']:
                x['id'] = x.pop('_id')
            return render(request, "authentication/rate-books-step.html", {'books': books['books']})
        else:
            messages.error(request, 'Error occured while getting books')
            return render(request, "authentication/rate-books-step.html", {'books': []})
        
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
            return render(request, "authentication/rate-books-step.html", {'books': books['books']})
        
                                
        else:
                messages.error(request, response.text)
                return render(request, "authentication/rate-books-step.html", {'books': []})
            
    except:
        return render(request, "authentication/rate-books-step.html", {'books': []})