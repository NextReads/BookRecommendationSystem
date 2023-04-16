from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from validate_email import validate_email
import json


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body) 
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid.'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Email is already taken.'}, status=409)
        return JsonResponse({'email_valid': True})
    
        
    
# Create your views here.
class UsernamesValidationView(View):
    def post(self, request):
        data = json.loads(request.body) 
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Username should only contain alphanumeric characters.'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Username is already taken.'}, status=409)
        return JsonResponse({'username_valid': True})

class SignupView(View):
    def get(self, request):
        return render(request, "authentication/signup.html", {})
    
    def post(self, request):
        # Get user data
        # validate data
        # create user
        # redirect to login page
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confrimPassword = request.POST.get('confirmPassword')
        context = {
            'fieldValues': request.POST
        }
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():

                if len(password) < 6:
                    messages.error(request, 'Password too short.')
                    return render(request, "authentication/signup.html", context)
                if password != confrimPassword:
                    messages.error(request, 'Passwords do not match.')
                    return render(request, "authentication/signup.html", context)
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.save()
                messages.success(request, 'Account created successfully.')
                #return redirect('login')
            else:
                messages.error(request, 'Email is already in use.')
                return render(request, "authentication/signup.html", {})
        return render(request, "authentication/signup.html", {})



        
    

class LoginView(View):
    def get(self, request):
        return render(request, "authentication/login.html", {})
    
class setGoalStepView(View):
    def get(self, request):
        return render(request, "authentication/set-goal-step.html", {})
    
class rateBooksStepView(View):
    def get(self, request):
        return render(request, "authentication/rate-books-step.html", {})


