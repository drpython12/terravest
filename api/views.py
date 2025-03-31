import json
import re
from datetime import datetime
import http.client
import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt

from yahoo_fin import stock_info  # Ensure yahoo_fin is installed

from .models import PortfolioStock, User, UserPreferences

ALPHA_VANTAGE_API_KEY = 'PNPAH7B7UT76I8OI'


def json_response(data, status=200):
    """Helper function to return JSON responses."""
    return JsonResponse(data, status=status)


def parse_json_request(request):
    """Parse JSON body from a request."""
    try:
        return json.loads(request.body)
    except json.JSONDecodeError:
        return None


def validate_signup_data(first_name, last_name, country, date_of_birth, email, password, confirm_password):
    """Validate user signup data."""
    errors = {}

    # Required field checks
    required_fields = {
        'first_name': first_name,
        'last_name': last_name,
        'country': country,
        'date_of_birth': date_of_birth,
        'email': email,
        'password': password,
        'confirm_password': confirm_password,
    }
    for field, value in required_fields.items():
        if not value:
            errors[field] = f'{field.replace("_", " ").capitalize()} is required.'

    # Email validation
    if email and User.objects.filter(email=email).exists():
        errors['email'] = 'Email is already registered.'
    try:
        validate_email(email)
    except ValidationError:
        errors['email'] = 'Invalid email format.'

    # Password validation
    password_pattern = re.compile(r'^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')
    if password and not password_pattern.match(password):
        errors['password'] = 'Password must contain at least 8 characters, a number, and a special character.'
    if password != confirm_password:
        errors['confirm_password'] = 'Passwords do not match.'

    # Date of birth validation
    try:
        dob = datetime.strptime(date_of_birth, "%Y-%m-%d")
        age = (datetime.today() - dob).days // 365
        if age < 18:
            errors['date_of_birth'] = 'You must be at least 18 years old to sign up.'
    except ValueError:
        errors['date_of_birth'] = 'Invalid date format.'

    return errors


def create_user(first_name, middle_name, last_name, country, date_of_birth, email, password):
    """Create a new user."""
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
    """Handle user signup."""
    if request.method == 'POST':
        data = parse_json_request(request)
        if not data:
            return json_response({'success': False, 'errors': 'Invalid JSON'}, status=400)

        errors = validate_signup_data(
            data.get('first_name'),
            data.get('last_name'),
            data.get('country'),
            data.get('date_of_birth'),
            data.get('email'),
            data.get('password'),
            data.get('confirm_password'),
        )
        if errors:
            return json_response({'success': False, 'errors': errors}, status=400)

        create_user(
            data.get('first_name'),
            data.get('middle_name', ''),
            data.get('last_name'),
            data.get('country'),
            data.get('date_of_birth'),
            data.get('email'),
            data.get('password'),
        )
        return json_response({'success': True, 'message': 'Account successfully created! Redirecting...'})

    return render(request, 'signup.html')


@csrf_exempt
def check_user_exists(request):
    """Check if a user exists by email."""
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
    """Handle user login."""
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
        if user:
            login(request, user)
            redirect_url = '/account/preferences/' if not user.preferences_completed else '/dashboard/'
            return json_response({'success': True, 'redirect': redirect_url})
        else:
            errors['login'] = 'Invalid email or password.'

        return json_response({'success': False, 'errors': errors}, status=400)

    return render(request, 'login.html')


@login_required
def app_data(request):
    """Return application data for the logged-in user."""
    user = request.user
    return json_response({
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
    """Log out the user."""
    logout(request)
    return json_response({'success': True, 'redirect': '/account/login/'})


@csrf_exempt
@login_required
def preferences_view(request):
    """Handle user preferences."""
    user = request.user

    if request.method == 'GET':
        preferences = UserPreferences.objects.filter(user=user).first()
        if preferences:
            return json_response({'success': True, 'preferences': preferences.to_dict()})
        return json_response({'success': True, 'preferences': {}})

    if request.method == 'POST':
        data = parse_json_request(request)
        if not data:
            return json_response({'success': False, 'errors': 'Invalid JSON'}, status=400)

        required_fields = ['riskLevel', 'investmentStrategy', 'sentimentAnalysis', 'transparencyLevel']
        if not all(data.get(field) for field in required_fields):
            return json_response({'success': False, 'errors': 'All required fields must be filled'}, status=400)

        preferences, _ = UserPreferences.objects.get_or_create(user=user)
        preferences.update_from_dict(data)
        preferences.save()

        user.preferences_completed = True
        user.save()

        return json_response({'success': True, 'message': 'Preferences saved successfully'})

    return json_response({'error': 'Invalid request method'}, status=400)


@csrf_exempt
@login_required
def update_settings(request):
    """Update user settings."""
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


@login_required
def get_portfolio(request):
    """Get user's portfolio holdings."""
    user = request.user
    holdings = PortfolioStock.objects.filter(user=user).values()
    return JsonResponse(list(holdings), safe=False)


def get_stock_price(request):
    """Fetch live stock price."""
    symbol = request.GET.get("symbol", "").strip().upper()
    if not symbol:
        return json_response({"error": "Symbol is required"}, status=400)
    
    connection = http.client.HTTPSConnection("yahoo-finance-real-time1.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': "c4cf9f510cmsh80ee50ea6a7d2b3p171c27jsnab5350889c90",
        'x-rapidapi-host': "yahoo-finance-real-time1.p.rapidapi.com"
    }

    connection.request("GET", f"/stock/get-quote-summary?symbol={symbol}&lang=en-US&region=US", headers=headers)
    response = connection.getresponse()
    data = response.read().decode("utf-8")
    json_data = json.loads(data)
    
    # Extract the regularMarketPrice field
    price = json_data["quoteSummary"]["result"][0]["price"]["regularMarketPrice"]
    
    return json_response({"symbol": symbol, "price": round(price, 2)})

@csrf_exempt
@login_required
def add_stock(request):
    """Add a stock to the user's portfolio."""
    if request.method == "POST":
        data = parse_json_request(request)
        if not data:
            return json_response({"error": "Invalid JSON"}, status=400)

        symbol = data.get("symbol")
        company_name = data.get("name")  # New field
        shares = data.get("shares")
        amount_invested = data.get("amountInvested")
        price_bought_at = data.get("priceBoughtAt")
        user = request.user

        if not symbol or not company_name or (shares is None and amount_invested is None):
            return json_response({"error": "Invalid data"}, status=400)

        # Calculate missing values
        if shares is None:
            shares = float(amount_invested) / float(price_bought_at)
        elif amount_invested is None:
            amount_invested = float(shares) * float(price_bought_at)

        stock, created = PortfolioStock.objects.get_or_create(
            user=user, symbol=symbol,
            defaults={
                "company_name": company_name,  # Save company name
                "shares": shares,
                "amount_invested": amount_invested,
                "price_bought_at": price_bought_at,
            }
        )

        if not created:
            stock.shares += shares
            stock.amount_invested += amount_invested
            stock.price_bought_at = price_bought_at
            stock.save()

        return json_response({"message": "Stock added successfully"})

    return json_response({"error": "Invalid request method"}, status=400)


@csrf_exempt
@login_required
def remove_stock(request, stock_id):
    """Remove a stock from the user's portfolio."""
    stock = get_object_or_404(PortfolioStock, id=stock_id, user=request.user)
    stock.delete()
    return json_response({"message": "Stock removed successfully"})


@csrf_exempt
def search_company(request):
    """Search for companies using Alpha Vantage."""
    query = request.GET.get("query", "").strip()
    if not query:
        return json_response({"error": "No query provided"}, status=400)

    try:
        url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={query}&apikey={ALPHA_VANTAGE_API_KEY}'
        response = requests.get(url)
        data = response.json()

        if "bestMatches" not in data:
            return json_response({"error": "No results found"}, status=404)

        results = [
            {
                "symbol": item["1. symbol"],
                "name": item["2. name"],
                "region": item["4. region"],
                "currency": item["8. currency"],
                "matchScore": float(item["9. matchScore"])
            }
            for item in data["bestMatches"]
        ]
        results.sort(key=lambda x: x["matchScore"], reverse=True)

        return json_response({"results": results})
    except Exception as e:
        return json_response({"error": str(e)}, status=500)