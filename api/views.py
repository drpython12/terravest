from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json
import re
from .models import User
from django.contrib.auth.decorators import login_required

def json_response(data, status=200):
    return JsonResponse(data, status=status)

def parse_json_request(request):
    try:
        return json.loads(request.body)
    except json.JSONDecodeError:
        return None

def validate_signup_data(first_name, last_name, country, date_of_birth, email, password, confirm_password):
    errors = {}

    if not first_name:
        errors['first_name'] = 'First name is required.'
    if not last_name:
        errors['last_name'] = 'Last name is required.'
    if not country:
        errors['country'] = 'Country is required.'
    if not date_of_birth:
        errors['date_of_birth'] = 'Date of birth is required.'
    if not email:
        errors['email'] = 'Email is required.'
    if not password:
        errors['password'] = 'Password is required.'
    if not confirm_password:
        errors['confirm_password'] = 'Confirm password is required.'

    if User.objects.filter(email=email).exists():
        errors['email'] = 'Email is already registered.'

    try:
        validate_email(email)
    except ValidationError:
        errors['email'] = 'Invalid email format.'

    password_pattern = re.compile(r'^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')
    if not password_pattern.match(password):
        errors['password'] = 'Password must contain at least 8 characters, a number, and a special character.'

    if password != confirm_password:
        errors['confirm_password'] = 'Passwords do not match.'

    try:
        dob = datetime.strptime(date_of_birth, "%Y-%m-%d")
        today = datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        if age < 18:
            errors['dob'] = 'You must be at least 18 years old to sign up.'
    except ValueError:
        errors['dob'] = 'Invalid date format.'

    return errors

def create_user(first_name, middle_name, last_name, country, date_of_birth, email, password):
    user = User(
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
        country=country,
        date_of_birth=date_of_birth,
        email=email,
        password=make_password(password),
    )
    user.save()
    return user

@csrf_exempt
def signup_view(request):
    if request.method == 'POST':
        data = parse_json_request(request)
        if not data:
            return json_response({'success': False, 'errors': 'Invalid JSON'}, status=400)

        first_name = data.get('first_name')
        middle_name = data.get('middle_name', '')
        last_name = data.get('last_name')
        country = data.get('country')
        date_of_birth = data.get('date_of_birth')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        errors = validate_signup_data(first_name, last_name, country, date_of_birth, email, password, confirm_password)
        if errors:
            return json_response({'success': False, 'errors': errors}, status=400)

        create_user(first_name, middle_name, last_name, country, date_of_birth, email, password)
        return json_response({'success': True, 'message': 'Account successfully created! Redirecting...'})
    return render(request, 'signup.html')

@csrf_exempt
def check_user_exists(request):
    if request.method == 'POST':
        data = parse_json_request(request)
        if not data:
            return json_response({'exists': False, 'error': 'Invalid JSON'}, status=400)

        email = data.get('email')
        if not email:
            return json_response({'exists': False, 'error': 'Email is required'}, status=400)

        exists = User.objects.filter(email=email).exists()
        return json_response({'exists': exists})
    return json_response({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = parse_json_request(request)
        if not data:
            return json_response({'success': False, 'errors': 'Invalid JSON'}, status=400)

        email = data.get('email')
        password = data.get('password')

        errors = {}
        try:
            validate_email(email)
        except ValidationError:
            errors['email'] = 'Invalid email format.'

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            if not user.preferences_completed:
                return json_response({'success': True, 'redirect': '/account/preferences/'})
            return json_response({'success': True, 'redirect': '/dashboard/'})
        else:
            errors['login'] = 'Invalid email or password.'

        if errors:
            return json_response({'success': False, 'errors': errors}, status=400)
    return render(request, 'login.html')

@login_required
def app_data(request):
    user = request.user
    return JsonResponse({
        'isLoggedIn': True,
        'user': {
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'preferences_completed': user.preferences_completed,
        }
    })

@csrf_exempt
def logout_view(request):
    logout(request)
    return json_response({'success': True, 'redirect': '/account/login/'})

@csrf_exempt
def preferences_view(request):
    if request.method == 'POST':
        data = parse_json_request(request)
        if not data:
            return json_response({'success': False, 'errors': 'Invalid JSON'}, status=400)

        investment_type = data.get('investmentType')
        risk_level = data.get('riskLevel')

        if not investment_type or not risk_level:
            return json_response({'success': False, 'errors': 'All fields are required'}, status=400)

        user = request.user
        user.investment_type = investment_type
        user.risk_level = risk_level
        user.preferences_completed = True
        user.save()

        return json_response({'success': True})
    return json_response({'error': 'Invalid request method'}, status=400)

@csrf_exempt
@login_required
def update_settings(request):
    if request.method == 'POST':
        data = parse_json_request(request)
        if not data:
            return json_response({'success': False, 'errors': 'Invalid JSON'}, status=400)

        user = request.user
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = data.get('email', user.email)
        user.save()

        return json_response({'success': True})
    return json_response({'error': 'Invalid request method'}, status=400)