from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json
import re
from .models import User, PortfolioStock, UserPreferences  # Ensure PortfolioStock model exists
from django.contrib.auth.decorators import login_required
import requests
from yahoo_fin import stock_info

ALPHA_VANTAGE_API_KEY = 'PNPAH7B7UT76I8OI'

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
@login_required
def preferences_view(request):
    user = request.user

    if request.method == 'GET':
        try:
            preferences = UserPreferences.objects.get(user=user)
            return json_response({
                'success': True,
                'preferences': {
                    'investment_type': preferences.investment_type,
                    'risk_level': preferences.risk_level,
                    'investment_strategy': preferences.investment_strategy,
                    'esg_factors': preferences.esg_factors,
                    'industry_preferences': preferences.industry_preferences,
                    'exclusions': preferences.exclusions,
                    'sentiment_analysis': preferences.sentiment_analysis,
                    'transparency_level': preferences.transparency_level,
                }
            })
        except UserPreferences.DoesNotExist:
            return json_response({'success': True, 'preferences': {}})

    if request.method == 'POST':
        data = parse_json_request(request)
        if not data:
            return json_response({'success': False, 'errors': 'Invalid JSON'}, status=400)

        # Extract preferences data from the request
        investment_type = data.get('investmentType')
        risk_level = data.get('riskLevel')
        investment_strategy = data.get('investmentStrategy')
        esg_factors = data.get('esgFactors', [])
        industry_preferences = data.get('industryPreferences', [])
        exclusions = data.get('exclusions', [])
        sentiment_analysis = data.get('sentimentAnalysis')
        transparency_level = data.get('transparencyLevel')

        # Validate required fields
        if not investment_type or not risk_level or not investment_strategy or not sentiment_analysis or not transparency_level:
            return json_response({'success': False, 'errors': 'All required fields must be filled'}, status=400)

        # Get or create the user's preferences
        preferences, _ = UserPreferences.objects.get_or_create(user=user)

        # Update the preferences
        preferences.investment_type = investment_type
        preferences.risk_level = risk_level
        preferences.investment_strategy = investment_strategy
        preferences.esg_factors = esg_factors
        preferences.industry_preferences = industry_preferences
        preferences.exclusions = exclusions
        preferences.sentiment_analysis = sentiment_analysis
        preferences.transparency_level = transparency_level
        preferences.save()

        # Mark the user's preferences as completed
        user.preferences_completed = True
        user.save()

        return json_response({'success': True, 'message': 'Preferences saved successfully'})

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

# Get user's portfolio holdings
@login_required
def get_portfolio(request):
    user = request.user
    holdings = PortfolioStock.objects.filter(user=user).values()
    return JsonResponse(list(holdings), safe=False)

# Fetch live stock price
def get_stock_price(request):
    symbol = request.GET.get("symbol", "").strip().upper()
    if not symbol:
        return JsonResponse({"error": "Symbol is required"}, status=400)

    try:
        price = stock_info.get_live_price(symbol)
        return JsonResponse({"symbol": symbol, "price": round(price, 2)})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

# Add a stock to the portfolio
@csrf_exempt
@login_required
def add_stock(request):
    if request.method == "POST":
        data = json.loads(request.body)
        symbol = data.get("symbol")
        shares = int(data.get("shares", 0))
        amount_invested = data.get("amountInvested")
        price_bought_at = data.get("priceBoughtAt")
        user = request.user

        if not symbol or shares <= 0:
            return JsonResponse({"error": "Invalid data"}, status=400)

        # Fetch stock price
        try:
            price = stock_info.get_live_price(symbol)
        except Exception:
            return JsonResponse({"error": "Failed to fetch stock price"}, status=400)

        # Save to portfolio
        stock, created = PortfolioStock.objects.get_or_create(
            user=user, symbol=symbol,
            defaults={"shares": shares, "price": price, "amount_invested": amount_invested, "price_bought_at": price_bought_at}
        )

        if not created:
            stock.shares += shares
            stock.amount_invested = amount_invested
            stock.price_bought_at = price_bought_at
            stock.save()

        return JsonResponse({"message": "Stock added successfully"})

# Remove a stock from the portfolio
@csrf_exempt
@login_required
def remove_stock(request, stock_id):
    stock = get_object_or_404(PortfolioStock, id=stock_id, user=request.user)
    stock.delete()
    return JsonResponse({"message": "Stock removed successfully"})

# Search for companies using Alpha Vantage
@csrf_exempt
def search_company(request):
    """Fetch matching company names from Alpha Vantage."""
    company = request.GET.get("query", "").strip()
    print(f"Query received: {company}")  # Debugging log
    if not company:
        return JsonResponse({"error": "No query provided"}, status=400)

    try:
        url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={company}&apikey={ALPHA_VANTAGE_API_KEY}'
        print(f"Requesting Alpha Vantage API: {url}")  # Debugging log
        r = requests.get(url)
        print(f"Alpha Vantage response status: {r.status_code}")  # Debugging log
        print(f"Alpha Vantage response: {r.text}")  # Debugging log

        data = r.json()
        if "bestMatches" not in data:
            return JsonResponse({"error": "No results found"}, status=404)

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

        # Sort results by match score in descending order
        results.sort(key=lambda x: x["matchScore"], reverse=True)

        return JsonResponse({"results": results})
    except KeyError as e:
        print(f"KeyError: {e}")  # Debugging log
        return JsonResponse({"error": f"Unexpected response format: {str(e)}"}, status=500)
    except Exception as e:
        print(f"Exception: {e}")  # Debugging log
        return JsonResponse({"error": str(e)}, status=500)