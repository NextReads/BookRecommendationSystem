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
        firstName = "nouranTest"
        lastName = "nouranTest"
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
        # if not User.objects.filter(username=username).exists():
        #     if not User.objects.filter(email=email).exists():

        #         if len(password) < 6:
        #             messages.error(request, 'Password too short.')
        #             return render(request, "authentication/signup.html", context)
        #         if password != confrimPassword:
        #             messages.error(request, 'Passwords do not match.')
        #             return render(request, "authentication/signup.html", context)
        #         user = User.objects.create_user(username=username, email=email)
        #         user.set_password(password)
        #         user.save()
        #         messages.success(request, 'Account created successfully.')
        #         #return redirect('login')
        #     else:
        #         messages.error(request, 'Email is already in use.')
        #         return render(request, "authentication/signup.html", {})
        # return render(request, "authentication/signup.html", {})


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
        
        # if password and username:
        #     user = auth.authenticate(username=username, password=password)
        #     print("user", user)
        #     if user:
        #         auth.login(request, user)
        #         #messages.success(request, 'You are now logged in.')
        #         #return render(request, "authentication/login.html", context)
        #         return redirect("set-goal-step")
        #     else:
        #         messages.error(request, 'Invalid credentials.')
        #         return render(request, "authentication/login.html", context)
        # else:
        #     messages.error(request, 'Please fill all fields.')
        #     return render(request, "authentication/login.html", context)

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
                print("An error occurred while making the request. Please try again later.") 

            try:
                booksResposne = requests.get('http://localhost:80/api/books/getbooks?page='+str(page))
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
            except RequestException as e:
                print("An error occurred while making the request. Please try again later.")

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
        

