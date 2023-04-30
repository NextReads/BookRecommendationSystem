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

class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body) 
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid.'}, status=400)
        # if User.objects.filter(email=email).exists():
        #     return JsonResponse({'email_error': 'Email is already taken.'}, status=409)
        return JsonResponse({'email_valid': True})
           
    
# Create your views here.
class UsernamesValidationView(View):
    def post(self, request):
        data = json.loads(request.body) 
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Username should only contain alphanumeric characters.'}, status=400)
        # if User.objects.filter(username=username).exists():
        #     return JsonResponse({'username_error': 'Username is already taken.'}, status=409)
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
        response = requests.post('https://nextreadsbackend.azurewebsites.net/api/users', json=data)
        if response.status_code == 201:
            userToken = response.headers['x-auth-token']
            #save token in session
            request.session['token'] = userToken
            messages.success(request, response.text)
            return redirect('set-goal-step')
        else:
            messages.error(request, response.text)
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
            response = requests.post('https://nextreadsbackend.azurewebsites.net/api/users/login', json=data)
            

            if response.status_code == 201:
                userToken = response.headers['x-auth-token']
                #save token in session
                request.session['token'] = userToken
                #messages.success(request, response.text)
                return redirect('userProfile:userhome')
            else:
                messages.error(request, response.text)
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
        # booksResposne = requests.get('https://nextreadsbackend.azurewebsites.net/api/books')
        # if booksResposne.status_code == 200:
           
        #   books = booksResposne.json()

            # context = {
            #     'books': books

            # }
            context = {
                'books': [
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
            }
            if context:
                return render(request, "authentication/rate-books-step.html", context)
            else:
                messages.error(request, "mfish books")
                return render(request, "authentication/rate-books-step.html", {})
        # else:
        #     messages.error(request, booksResposne.text)
        #     return render(request, "authentication/rate-books-step.html", {})
class rateBook(View):

    def post(self, request):
        bookId = request.POST.get('book_id')
        rating = request.POST.get('rating')
        print("bookId", bookId)
        print("rating", rating)
        print("token", request.session['token'])
        
        # if bookId and rating:
        #     data={'bookId': bookId, 'rating': rating}
        #     response = requests.post('https://nextreadsbackend.azurewebsites.net/api/books/rate', json=data)
        #     if response.status_code == 201:
        #         messages.success(request, response.text)
        #         return redirect('set-goal-step')
        #     else:
        #         messages.error(request, response.text)
        #         return redirect('rate-books-step')
        # else:
        #     messages.error(request, 'Please fill all fields.')
        return redirect('rate-books-step')

