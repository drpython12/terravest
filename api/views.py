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
from django.db.models import Avg, Max, Min, Sum, F, Case, When, FloatField
from django.core.paginator import Paginator
from .models import PortfolioStock, User, UserPreferences, ESGCompany, ESGMetric
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

ALPHA_VANTAGE_API_KEY = 'PNPAH7B7UT76I8OI'


def json_response(data, status=200):
    """Helper function to return JSON responses."""
    return JsonResponse(data, status=status, safe=isinstance(data, dict))


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


@csrf_exempt
@login_required
def get_esg_data(request):
    """Fetch ESG data for companies in the user's portfolio."""
    if request.method != "GET":
        return json_response({"error": "Invalid request method"}, status=400)

    user = request.user
    portfolio_stocks = PortfolioStock.objects.filter(user=user)
    total_portfolio_value = portfolio_stocks.aggregate(total_value=Sum(F('shares') * F('price_bought_at')))['total_value'] or 0

    esg_data = []
    for stock in portfolio_stocks:
        company = ESGCompany.objects.filter(ticker=stock.symbol).first()
        if not company:
            continue

        latest_year = get_latest_year_for_company(company)
        metrics = ESGMetric.objects.filter(company=company, year=latest_year)
        esg_scores = {
            "overall": get_metric_score(metrics, "ESGScore"),
            "environmental": get_metric_score(metrics, "EnvironmentPillarScore"),
            "social": get_metric_score(metrics, "SocialPillarScore"),
            "governance": get_metric_score(metrics, "GovernancePillarScore"),
            "subcategories": {
                "emissions": get_metric_score(metrics, "ESGEmissionsScore"),
                "resource_use": get_metric_score(metrics, "ESGResourceUseScore"),
                "innovation": get_metric_score(metrics, "ESGInnovationScore"),
                "human_rights": get_metric_score(metrics, "ESGHumanRightsScore"),
                "product_responsibility": get_metric_score(metrics, "ESGProductResponsibilityScore"),
                "workforce": get_metric_score(metrics, "ESGWorkforceScore"),
                "community": get_metric_score(metrics, "ESGCommunityScore"),
                "management": get_metric_score(metrics, "ESGManagementScore"),
                "shareholders": get_metric_score(metrics, "ESGShareholdersScore"),
                "csr_strategy": get_metric_score(metrics, "ESGCsrStrategyScore"),
            }
        }

        # Calculate the weight of the stock in the portfolio
        stock_value = stock.shares * stock.price_bought_at
        weight = stock_value / total_portfolio_value if total_portfolio_value > 0 else 0

        esg_data.append({
            "symbol": stock.symbol,
            "company_name": stock.company_name,
            "weight": weight,
            "esg_scores": esg_scores,
        })

    logger.info(f"User: {user.email}")
    logger.info(f"Portfolio Stocks: {portfolio_stocks}")
    logger.info(f"ESG Data: {esg_data}")

    return json_response({"esg_data": esg_data})


def get_portfolio_company_symbols(user):
    """Retrieve company symbols from the user's portfolio."""
    portfolio_stocks = PortfolioStock.objects.filter(user=user)
    return portfolio_stocks.values_list("symbol", flat=True)


def fetch_esg_data_for_companies(company_symbols):
    """Fetch ESG data for a list of company symbols."""
    companies = ESGCompany.objects.filter(ticker__in=company_symbols)
    esg_data = [get_company_esg_data(company) for company in companies]
    return esg_data


def get_company_esg_data(company):
    """Fetch ESG data for a single company."""
    latest_year = get_latest_year_for_company(company)
    metrics = ESGMetric.objects.filter(company=company, year=latest_year)
    overall_esg_score = get_metric_score(metrics, "ESGScore")  # Fetch overall ESG score
    return {
        "id": company.id,
        "company_name": company.name,
        "symbol": company.ticker,
        "overall_esg_score": overall_esg_score,  # Add overall ESG score
        "environmental": get_metric_score(metrics, "EnvironmentPillarScore"),
        "social": get_metric_score(metrics, "SocialPillarScore"),
        "governance": get_metric_score(metrics, "GovernancePillarScore"),
        "emissions": get_metric_score(metrics, "ESGEmissionsScore"),
        "resource_use": get_metric_score(metrics, "ESGResourceUseScore"),
        "innovation": get_metric_score(metrics, "ESGInnovationScore"),
        "human_rights": get_metric_score(metrics, "ESGHumanRightsScore"),
        "product_responsibility": get_metric_score(metrics, "ESGProductResponsibilityScore"),
        "workforce": get_metric_score(metrics, "ESGWorkforceScore"),
        "community": get_metric_score(metrics, "ESGCommunityScore"),
        "management": get_metric_score(metrics, "ESGManagementScore"),
        "shareholders": get_metric_score(metrics, "ESGShareholdersScore"),
        "csr_strategy": get_metric_score(metrics, "ESGCsrStrategyScore"),
    }


def get_latest_year_for_company(company):
    """Get the latest year for which ESG metrics are available for a company."""
    return ESGMetric.objects.filter(company=company).aggregate(latest_year=Max("year"))["latest_year"]


def get_metric_score(metrics, fieldname):
    """Fetch and normalize a specific ESG metric score."""
    metric = metrics.filter(fieldname=fieldname).first()
    return round(metric.valuescore * 100) if metric else 0


from decimal import Decimal

def get_weighted_esg_trends(portfolio_stocks, stock_values, total_portfolio_value):
    """Calculate weighted ESG trends for the portfolio."""
    if total_portfolio_value == 0:
        return {"ESGScore": [], "EnvironmentPillarScore": [], "SocialPillarScore": [], "GovernancePillarScore": []}

    esg_trends = {
        "ESGScore": {},
        "EnvironmentPillarScore": {},
        "SocialPillarScore": {},
        "GovernancePillarScore": {},
    }

    for stock in portfolio_stocks:
        try:
            company = ESGCompany.objects.filter(ticker=stock.symbol).first()
            if not company:
                continue

            metrics = ESGMetric.objects.filter(company=company)
            stock_value = stock_values.get(stock.symbol, 0)
            weight = Decimal(stock_value) / Decimal(total_portfolio_value)

            for metric in metrics:
                year = metric.year
                for category in esg_trends.keys():
                    if metric.fieldname == category:
                        if year not in esg_trends[category]:
                            esg_trends[category][year] = 0
                        esg_trends[category][year] += metric.valuescore * float(weight) * 100
        except Exception as e:
            logger.error(f"Error calculating ESG trends for {stock.symbol}: {e}")

    # Convert trends to sorted lists
    for category in esg_trends.keys():
        esg_trends[category] = sorted(
            [{"year": year, "score": round(score, 2)} for year, score in esg_trends[category].items()],
            key=lambda x: x["year"]
        )

    return esg_trends


def get_dashboard_data(request):
    """Fetch dashboard data for the logged-in user."""
    user = request.user
    logger.info(f"Fetching dashboard data for user: {user.email}")

    portfolio_stocks = PortfolioStock.objects.filter(user=user)
    logger.info(f"Portfolio stocks: {portfolio_stocks}")

    stock_values, total_portfolio_value = calculate_portfolio_value(portfolio_stocks)
    weighted_esg_score = calculate_weighted_esg_score(portfolio_stocks, stock_values, total_portfolio_value)
    portfolio_performance = calculate_portfolio_performance(portfolio_stocks, total_portfolio_value)
    esg_breakdown = calculate_esg_breakdown(portfolio_stocks)
    top_holdings = get_top_holdings(portfolio_stocks)
    esg_trends = get_weighted_esg_trends(portfolio_stocks, stock_values, total_portfolio_value)

    return json_response({
        "portfolio_value": float(total_portfolio_value),
        "overall_esg_score": round(weighted_esg_score * 100, 0) if total_portfolio_value > 0 else None,
        "portfolio_performance_change": round(portfolio_performance, 2),
        "esg_breakdown": esg_breakdown,
        "esg_trends": esg_trends,  # Include ESG trends
        "top_holdings": list(top_holdings),
    })


def calculate_portfolio_value(portfolio_stocks):
    """Calculate the total portfolio value and stock values."""
    total_portfolio_value = Decimal(0)
    stock_values = {}
    for stock in portfolio_stocks:
        try:
            live_price = fetch_live_stock_price(stock.symbol)
            stock_value = Decimal(live_price) * Decimal(stock.shares)
            stock_values[stock.symbol] = stock_value
            total_portfolio_value += stock_value
        except Exception as e:
            logger.error(f"Error fetching live price for {stock.symbol}: {e}")
    return stock_values, total_portfolio_value


def fetch_live_stock_price(symbol):
    """Fetch live stock price for a given symbol."""
    connection = http.client.HTTPSConnection("yahoo-finance-real-time1.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': "c4cf9f510cmsh80ee50ea6a7d2b3p171c27jsnab5350889c90",
        'x-rapidapi-host': "yahoo-finance-real-time1.p.rapidapi.com"
    }
    connection.request("GET", f"/stock/get-quote-summary?symbol={symbol}&lang=en-US&region=US", headers=headers)
    response = connection.getresponse()
    data = response.read().decode("utf-8")
    json_data = json.loads(data)
    return json_data["quoteSummary"]["result"][0]["price"]["regularMarketPrice"]


def calculate_weighted_esg_score(portfolio_stocks, stock_values, total_portfolio_value):
    """Calculate the weighted ESG score for the portfolio."""
    if total_portfolio_value == 0:
        return None  # Avoid division by zero and return None if the portfolio value is zero

    weighted_esg_score = Decimal(0)
    for stock in portfolio_stocks:
        try:
            # Fetch the latest ESG score for the stock
            esg_score = fetch_latest_esg_score(stock.symbol)
            if esg_score is not None:
                # Calculate the weight of the stock in the portfolio
                stock_value = stock_values.get(stock.symbol, 0)
                weight = Decimal(stock_value) / Decimal(total_portfolio_value)
                # Add the weighted ESG score to the total
                weighted_esg_score += Decimal(esg_score) * weight
        except Exception as e:
            logger.error(f"Error calculating ESG score for {stock.symbol}: {e}")
    return weighted_esg_score


def fetch_latest_esg_score(symbol):
    """Fetch the latest ESG score for a given stock symbol."""
    latest_year = ESGMetric.objects.filter(
        company__ticker=symbol,
        fieldname="ESGScore"
    ).aggregate(latest_year=Max('year'))['latest_year']

    if latest_year:
        metric = ESGMetric.objects.filter(
            company__ticker=symbol,
            fieldname="ESGScore",
            year=latest_year
        ).first()
        return metric.valuescore if metric else None
    return None


def calculate_portfolio_performance(portfolio_stocks, total_portfolio_value):
    """Calculate the portfolio performance."""
    total_invested = portfolio_stocks.aggregate(total_invested=Sum('amount_invested'))['total_invested'] or Decimal(0)
    if total_invested > 0:
        return ((total_portfolio_value - total_invested) / total_invested) * 100
    return 0


def calculate_esg_breakdown(portfolio_stocks):
    """Calculate the ESG breakdown for the portfolio."""
    return {
        "environmental": ESGMetric.objects.filter(
            company__ticker__in=portfolio_stocks.values_list('symbol', flat=True),
            pillar="Environmental"
        ).aggregate(avg_score=Avg('valuescore'))['avg_score'] or 0,
        "social": ESGMetric.objects.filter(
            company__ticker__in=portfolio_stocks.values_list('symbol', flat=True),
            pillar="Social"
        ).aggregate(avg_score=Avg('valuescore'))['avg_score'] or 0,
        "governance": ESGMetric.objects.filter(
            company__ticker__in=portfolio_stocks.values_list('symbol', flat=True),
            pillar="Governance"
        ).aggregate(avg_score=Avg('valuescore'))['avg_score'] or 0,
    }


def get_top_holdings(portfolio_stocks):
    """Get the top holdings in the portfolio."""
    return portfolio_stocks.annotate(
        esg_score=Case(
            When(symbol__in=ESGMetric.objects.values_list('company__ticker', flat=True), then=F('amount_invested')),
            default=0,
            output_field=FloatField()
        )
    ).values('company_name', 'symbol', 'shares', 'amount_invested')


import openai
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Set your OpenAI API key
openai.api_key = "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"

@csrf_exempt
@login_required
def chatgpt_advisor(request):
    """
    View to handle ChatGPT interactions for portfolio suitability.
    """
    if request.method == "POST":
        try:
            # Parse the request body
            body = json.loads(request.body)
            question = body.get("question", "")
            company = body.get("company", {})
            preferences = body.get("preferences", {})

            if not question or not company or not preferences:
                return JsonResponse({"error": "Invalid input data."}, status=400)

            # Construct the prompt for ChatGPT
            prompt = f"""
            You are a financial advisor specializing in ESG (Environmental, Social, and Governance) investing. 
            A user has asked the following question: "{question}"

            The company in question is:
            - Name: {company.get('name')}
            - Symbol: {company.get('symbol')}
            - Description: {company.get('description')}

            The company's ESG breakdown is as follows:
            - Environmental Score: {company.get('environmental_score', 'N/A')}
            - Social Score: {company.get('social_score', 'N/A')}
            - Governance Score: {company.get('governance_score', 'N/A')}

            The user's portfolio preferences are:
            {json.dumps(preferences, indent=2)}

            Provide a detailed, quantifiable response on how well this company aligns with the user's preferences. 
            Be concise and professional.
            """

            # Call OpenAI's GPT model
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=500,
                temperature=0.7,
            )

            # Extract the response text
            answer = response.choices[0].text.strip()

            # Return the response
            return JsonResponse({"answer": answer}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

@csrf_exempt
def get_company_esg_data(request, ticker):
    """Fetch ESG data for a single company based on its ticker."""
    try:
        # Fetch the company using the ticker
        company = get_object_or_404(ESGCompany, ticker=ticker)
        
        # Fetch ESG data for the company
        latest_year = get_latest_year_for_company(company)
        metrics = ESGMetric.objects.filter(company=company, year=latest_year)
        overall_esg_score = get_metric_score(metrics, "ESGScore")  # Fetch overall ESG score
        
        # Fetch historical ESG scores
        historical_metrics = ESGMetric.objects.filter(company=company, fieldname="ESGScore").order_by("year")
        historical_scores = [{"year": metric.year, "score": metric.valuescore * 100} for metric in historical_metrics]

        # Prepare the response data
        data = {
            "id": company.id,
            "Company Name": company.name,
            "Symbol": company.ticker,
            "Overall ESG Score": overall_esg_score,
            "Environmental": get_metric_score(metrics, "EnvironmentPillarScore"),
            "Social": get_metric_score(metrics, "SocialPillarScore"),
            "Governance": get_metric_score(metrics, "GovernancePillarScore"),
            "Emissions": get_metric_score(metrics, "ESGEmissionsScore"),
            "Resource Use": get_metric_score(metrics, "ESGResourceUseScore"),
            "Innovation": get_metric_score(metrics, "ESGInnovationScore"),
            "Human Rights": get_metric_score(metrics, "ESGHumanRightsScore"),
            "Product Responsibility": get_metric_score(metrics, "ESGProductResponsibilityScore"),
            "Workforce": get_metric_score(metrics, "ESGWorkforceScore"),
            "Community": get_metric_score(metrics, "ESGCommunityScore"),
            "Management": get_metric_score(metrics, "ESGManagementScore"),
            "Shareholders": get_metric_score(metrics, "ESGShareholdersScore"),
            "CSR Strategy": get_metric_score(metrics, "ESGCsrStrategyScore"),
            "Historical Scores": historical_scores  # Add historical ESG scores
        }
        
        # Fetch controversy data
        controversies = ESGMetric.objects.filter(company=company, fieldname="ControversyScore").order_by("-year")
        controversy_data = [{"year": metric.year, "score": metric.valuescore * 100} for metric in controversies]

        # Fetch benchmark data
        # industry_benchmark = ESGMetric.objects.filter(
        #     company__industry=company.industry, fieldname="ESGScore"
        # ).aggregate(avg_score=Avg("valuescore"))["avg_score"]

        data["controversy_data"] = controversy_data
        # data["industry_benchmark"] = round(industry_benchmark * 100, 2) if industry_benchmark else None
        
        # Generate AI summary
        # ai_summary_prompt = f"""
        # Provide a concise summary of the ESG performance for the company:
        # - Name: {company.name}
        # - Environmental Score: {data['environmental']}
        # - Social Score: {data['social']}
        # - Governance Score: {data['governance']}
        # """
        # ai_summary = generate_ai_summary(ai_summary_prompt)  # Call a helper function to generate the summary
        # data["ai_summary"] = ai_summary
        
        return JsonResponse(data, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def generate_ai_summary(prompt):
    """Generate an AI summary using OpenAI."""
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            temperature=0.7,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        logger.error(f"Error generating AI summary: {e}")
        return "Unable to generate summary at this time."


def calculate_esg_contribution(company, portfolio_weight):
    """Calculate ESG contribution to investment strategy."""
    return {
        "environmental": company.environmental * portfolio_weight,
        "social": company.social * portfolio_weight,
        "governance": company.governance * portfolio_weight,
    }