from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json
import re
from .models import User

@csrf_exempt
def signup_view(request):
    """
    Handle user signup requests.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'errors': 'Invalid JSON'}, status=400)

        print("Received POST request with data:", data)
        
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
            return JsonResponse({'success': False, 'errors': errors}, status=400)

        create_user(first_name, middle_name, last_name, country, date_of_birth, email, password)
        return JsonResponse({'success': True, 'message': 'Account successfully created! Redirecting...'})
    return render(request, 'signup.html')


def validate_signup_data(first_name, last_name, country, date_of_birth, email, password, confirm_password):
    """
    Validate the signup data provided by the user.
    """
    errors = {}

    # Check for missing fields
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

    # Check if email is already registered
    if User.objects.filter(email=email).exists():
        errors['email'] = 'Email is already registered.'

    # Validate email format
    try:
        validate_email(email)
    except ValidationError:
        errors['email'] = 'Invalid email format.'

    # Validate password format
    password_pattern = re.compile(r'^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')
    if not password_pattern.match(password):
        errors['password'] = 'Password must contain at least 8 characters, a number, and a special character.'

    # Check if passwords match
    if password != confirm_password:
        errors['confirm_password'] = 'Passwords do not match.'

    # Validate age (must be 18+)
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
    """
    Create a new user with the provided data.
    """
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
def check_user_exists(request):
    """
    Check if a user exists by email.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            if not email:
                return JsonResponse({'exists': False, 'error': 'Email is required'}, status=400)

            exists = User.objects.filter(email=email).exists()
            return JsonResponse({'exists': exists})
        except json.JSONDecodeError:
            return JsonResponse({'exists': False, 'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


def login_view(request):
    """
    Handle user login requests.
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        errors = {}

        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            errors['email'] = 'Invalid email format.'

        # Authenticate user
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True, 'message': 'Login successful! Redirecting...'})
        else:
            errors['login'] = 'Invalid email or password.'

        # If any errors exist, return them
        if errors:
            return JsonResponse({'success': False, 'errors': errors}, status=400)

    return render(request, 'login.html')