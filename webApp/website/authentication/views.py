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
        messages.success(request, 'Account created successfully.')
        messages.error (request, 'Error creating your account.')
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


