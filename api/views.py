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
from django.db.models import Avg, Max, Sum, F, Case, When, FloatField
from .models import PortfolioStock, User, UserPreferences, ESGCompany, ESGMetric
from django.core.cache import cache
import logging
from rest_framework.decorators import api_view
from django.conf import settings
from openai import OpenAI
from pydantic import BaseModel, conlist
from typing import List
import uuid
from decimal import Decimal
from django.utils.decorators import method_decorator
from threading import Thread

client = OpenAI(api_key=settings.OPENAI_API_KEY)
logger = logging.getLogger(__name__)
ALPHA_VANTAGE_API_KEY = settings.ALPHA_VANTAGE_API_KEY

def json_response(data, status=200):
    return JsonResponse(data, status=status, safe=isinstance(data, dict))

def parse_json_request(request):
    try:
        return json.loads(request.body)
    except json.JSONDecodeError:
        return None

def validate_signup_data(first_name, last_name, country, date_of_birth, email, password, confirm_password):
    errors = {}
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
    if email and User.objects.filter(email=email).exists():
        errors['email'] = 'Email is already registered.'
    try:
        validate_email(email)
    except ValidationError:
        errors['email'] = 'Invalid email format.'
    password_pattern = re.compile(r'^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')
    if password and not password_pattern.match(password):
        errors['password'] = 'Password must contain at least 8 characters, a number, and a special character.'
    if password != confirm_password:
        errors['confirm_password'] = 'Passwords do not match.'
    try:
        dob = datetime.strptime(date_of_birth, "%Y-%m-%d")
        age = (datetime.today() - dob).days // 365
        if age < 18:
            errors['date_of_birth'] = 'You must be at least 18 years old to sign up.'
    except ValueError:
        errors['date_of_birth'] = 'Invalid date format.'
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
        if user:
            login(request, user)
            return json_response({
                'success': True,
                'redirect': '/account/preferences/' if not user.preferences_completed else '/dashboard/',
                'preferences_completed': user.preferences_completed,
            })
        else:
            errors['login'] = 'Invalid email or password.'
        return json_response({'success': False, 'errors': errors}, status=400)
    return render(request, 'login.html')

@login_required
def app_data(request):
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
    logout(request)
    return json_response({'success': True, 'redirect': '/account/login/'})

@csrf_exempt
@login_required
def preferences_view(request):
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
    user = request.user
    holdings = PortfolioStock.objects.filter(user=user).values()
    return JsonResponse(list(holdings), safe=False)

def get_stock_price(request):
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
    price = json_data["quoteSummary"]["result"][0]["price"]["regularMarketPrice"]
    return json_response({"symbol": symbol, "price": round(price, 2)})

@csrf_exempt
@login_required
def add_stock(request):
    if request.method == "POST":
        data = parse_json_request(request)
        if not data:
            return json_response({"error": "Invalid JSON"}, status=400)
        symbol = data.get("symbol")
        company_name = data.get("name")
        shares = data.get("shares")
        amount_invested = data.get("amountInvested")
        price_bought_at = data.get("priceBoughtAt")
        user = request.user
        if not symbol or not company_name or (shares is None and amount_invested is None):
            return json_response({"error": "Invalid data"}, status=400)
        if shares is None:
            shares = float(amount_invested) / float(price_bought_at)
        elif amount_invested is None:
            amount_invested = float(shares) * float(price_bought_at)
        stock, created = PortfolioStock.objects.get_or_create(
            user=user, symbol=symbol,
            defaults={
                "company_name": company_name,
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
    stock = get_object_or_404(PortfolioStock, id=stock_id, user=request.user)
    stock.delete()
    return json_response({"message": "Stock removed successfully"})

@csrf_exempt
def search_company(request):
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
            for item in data["bestMatches"] if item["4. region"] == "United States"
        ]
        results.sort(key=lambda x: x["matchScore"], reverse=True)
        return json_response({"results": results})
    except Exception as e:
        return json_response({"error": str(e)}, status=500)

@csrf_exempt
@login_required
def get_esg_data(request):
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
        stock_value = stock.shares * stock.price_bought_at
        weight = stock_value / total_portfolio_value if total_portfolio_value > 0 else 0
        esg_data.append({
            "symbol": stock.symbol,
            "company_name": stock.company_name,
            "weight": weight,
            "esg_scores": esg_scores,
        })
    return json_response({"esg_data": esg_data})

def get_portfolio_company_symbols(user):
    portfolio_stocks = PortfolioStock.objects.filter(user=user)
    return portfolio_stocks.values_list("symbol", flat=True)

def fetch_esg_data_for_companies(company_symbols):
    companies = ESGCompany.objects.filter(ticker__in=company_symbols)
    esg_data = [get_company_esg_data(company) for company in companies]
    return esg_data

def get_latest_year_for_company(company):
    return ESGMetric.objects.filter(company=company).aggregate(latest_year=Max("year"))["latest_year"]

def get_metric_score(metrics, fieldname):
    metric = metrics.filter(fieldname=fieldname).first()
    return round(metric.valuescore * 100) if metric else 0

def get_weighted_esg_trends(portfolio_stocks, stock_values, total_portfolio_value):
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
            pass
    for category in esg_trends.keys():
        esg_trends[category] = sorted(
            [{"year": year, "score": round(score, 2)} for year, score in esg_trends[category].items()],
            key=lambda x: x["year"]
        )
    return esg_trends

def get_dashboard_data(request):
    user = request.user
    portfolio_stocks = PortfolioStock.objects.filter(user=user)
    stock_values, total_portfolio_value = calculate_portfolio_value(portfolio_stocks)

    # Calculate weighted ESG scores
    weighted_esg_scores = {
        "environmental": 0,
        "social": 0,
        "governance": 0,
        "overall": 0,
    }
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
            weight = Decimal(stock_value) / Decimal(total_portfolio_value) if total_portfolio_value > 0 else 0

            # Add weighted ESG scores
            weighted_esg_scores["environmental"] += get_metric_score(metrics, "EnvironmentPillarScore") * weight
            weighted_esg_scores["social"] += get_metric_score(metrics, "SocialPillarScore") * weight
            weighted_esg_scores["governance"] += get_metric_score(metrics, "GovernancePillarScore") * weight
            weighted_esg_scores["overall"] += get_metric_score(metrics, "ESGScore") * weight

            # Add ESG trends
            for metric in metrics:
                year = metric.year
                fieldname = metric.fieldname
                if fieldname in esg_trends:
                    if year not in esg_trends[fieldname]:
                        esg_trends[fieldname][year] = 0
                    esg_trends[fieldname][year] += metric.valuescore * weight

        except Exception as e:
            pass

    # Format ESG trends for the frontend
    formatted_esg_trends = {
        "ESGScore": [{"year": year, "score": round(score, 2)} for year, score in esg_trends["ESGScore"].items()],
        "EnvironmentPillarScore": [{"year": year, "score": round(score, 2)} for year, score in esg_trends["EnvironmentPillarScore"].items()],
        "SocialPillarScore": [{"year": year, "score": round(score, 2)} for year, score in esg_trends["SocialPillarScore"].items()],
        "GovernancePillarScore": [{"year": year, "score": round(score, 2)} for year, score in esg_trends["GovernancePillarScore"].items()],
    }

    # Normalize values
    overall_esg_score = round(weighted_esg_scores["overall"], 0) if total_portfolio_value > 0 else None
    portfolio_performance_change = round(calculate_portfolio_performance(portfolio_stocks, total_portfolio_value), 2)

    return json_response({
        "portfolio_value": float(total_portfolio_value),
        "overall_esg_score": overall_esg_score,  # Rounded to a full number
        "portfolio_performance_change": portfolio_performance_change,  # Rounded to 2 decimal places
        "esg_breakdown": {
            "environmental": round(weighted_esg_scores["environmental"] * 100, 2),
            "social": round(weighted_esg_scores["social"] * 100, 2),
            "governance": round(weighted_esg_scores["governance"] * 100, 2),
        },
        "esg_trends": formatted_esg_trends,
        "top_holdings": list(get_top_holdings(portfolio_stocks)),
    })

def calculate_portfolio_value(portfolio_stocks):
    total_portfolio_value = Decimal(0)
    stock_values = {}
    for stock in portfolio_stocks:
        try:
            live_price = fetch_live_stock_price(stock.symbol)
            stock_value = Decimal(live_price) * Decimal(stock.shares)
            stock_values[stock.symbol] = stock_value
            total_portfolio_value += stock_value
        except Exception as e:
            pass
    return stock_values, total_portfolio_value

def fetch_live_stock_price(symbol):
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
    if total_portfolio_value == 0:
        return None
    weighted_esg_score = Decimal(0)
    for stock in portfolio_stocks:
        try:
            esg_score = fetch_latest_esg_score(stock.symbol)
            if esg_score is not None:
                stock_value = stock_values.get(stock.symbol, 0)
                weight = Decimal(stock_value) / Decimal(total_portfolio_value)
                weighted_esg_score += Decimal(esg_score) * weight
        except Exception as e:
            pass
    return weighted_esg_score

def fetch_latest_esg_score(symbol):
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
    total_invested = portfolio_stocks.aggregate(total_invested=Sum('amount_invested'))['total_invested'] or Decimal(0)
    if total_invested > 0:
        return ((total_portfolio_value - total_invested) / total_invested) * 100
    return 0

def calculate_esg_breakdown(portfolio_stocks):
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
    return portfolio_stocks.annotate(
        esg_score=Case(
            When(symbol__in=ESGMetric.objects.values_list('company__ticker', flat=True), then=F('amount_invested')),
            default=0,
            output_field=FloatField()
        )
    ).values('company_name', 'symbol', 'shares', 'amount_invested')

@csrf_exempt
@login_required
def chatgpt_advisor(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            question = body.get("question", "")
            company = body.get("company", {})
            preferences = body.get("preferences", {})
            if not question or not company or not preferences:
                return JsonResponse({"error": "Invalid input data."}, status=400)
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
            response = client.completions.create(engine="text-davinci-003",
            prompt=prompt,
            max_tokens=500,
            temperature=0.7)
            answer = response.choices[0].text.strip()
            return JsonResponse({"answer": answer}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
    return JsonResponse({"error": "Invalid request method."}, status=405)

@csrf_exempt
def get_company_esg_data(request, ticker):
    try:
        company = get_object_or_404(ESGCompany, ticker=ticker)
        latest_year = get_latest_year_for_company(company)
        metrics = ESGMetric.objects.filter(company=company, year=latest_year)
        overall_esg_score = get_metric_score(metrics, "ESGScore")
        historical_metrics = ESGMetric.objects.filter(company=company).order_by("year")
        historical_scores = []
        for year in historical_metrics.values_list("year", flat=True).distinct():
            year_metrics = historical_metrics.filter(year=year)
            historical_scores.append({
                "year": year,
                "score": get_metric_score(year_metrics, "ESGScore"),
                "environmental": get_metric_score(year_metrics, "EnvironmentPillarScore"),
                "social": get_metric_score(year_metrics, "SocialPillarScore"),
                "governance": get_metric_score(year_metrics, "GovernancePillarScore"),
            })
        kpi_drilldown_data = {
            "Environment": {
                "color": "#6B46C1",
                "score": get_metric_score(metrics, "EnvironmentPillarScore"),
                "details": {
                    "Emissions": get_metric_score(metrics, "ESGEmissionsScore"),
                    "Resource Use": get_metric_score(metrics, "ESGResourceUseScore"),
                    "Innovation": get_metric_score(metrics, "ESGInnovationScore"),
                },
            },
            "Social": {
                "color": "#D69E2E",
                "score": get_metric_score(metrics, "SocialPillarScore"),
                "details": {
                    "Human Rights": get_metric_score(metrics, "ESGHumanRightsScore"),
                    "Product Responsibility": get_metric_score(metrics, "ESGProductResponsibilityScore"),
                    "Workforce": get_metric_score(metrics, "ESGWorkforceScore"),
                    "Community": get_metric_score(metrics, "ESGCommunityScore"),
                },
            },
            "Governance": {
                "color": "#2F855A",
                "score": get_metric_score(metrics, "GovernancePillarScore"),
                "details": {
                    "Management": get_metric_score(metrics, "ESGManagementScore"),
                    "Shareholders": get_metric_score(metrics, "ESGShareholdersScore"),
                    "CSR Strategy": get_metric_score(metrics, "ESGCsrStrategyScore"),
                },
            }
        }
        controversies = ESGMetric.objects.filter(company=company, fieldname__icontains="ControversiesCount").order_by("year")
        controversy_data = {}
        controversy_categories = set()
        for metric in controversies:
            year = metric.year
            if year not in controversy_data:
                controversy_data[year] = {}
            controversy_data[year][metric.fieldname] = {
                "value": metric.value,
                "valuescore": round(metric.valuescore * 100, 2) if metric.valuescore else None,
            }
            controversy_categories.add(metric.fieldname)
        controversy_categories = sorted(controversy_categories)
        url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={ticker}&apikey={ALPHA_VANTAGE_API_KEY}'
        response = requests.get(url)
        data = response.json()
        if "bestMatches" not in data:
            return json_response({"error": "No results found"}, status=404)
        company_name = data["bestMatches"][0]["2. name"]
        data = {
            "id": company.orgperm_id,
            "Company Name": company_name,
            "Symbol": company.ticker,
            "Overall ESG Score": overall_esg_score,
            "KPI Drilldown": kpi_drilldown_data,
            "Historical Scores": historical_scores,
            "Controversy Data": controversy_data,
            "Controversy Categories": controversy_categories,
        }
        return JsonResponse(data, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def calculate_esg_contribution(company, portfolio_weight):
    return {
        "environmental": company.environmental * portfolio_weight,
        "social": company.social * portfolio_weight,
        "governance": company.governance * portfolio_weight,
    }

class Articles(BaseModel):
    title: str
    description: str
    url: str
    source: str
    date: str

class NewsFormat(BaseModel):
    articles: conlist(Articles)

@csrf_exempt
@login_required
def fetch_esg_news(request):
    try:
        company_name = request.GET.get("company_name")
        if not company_name or not isinstance(company_name, str):
            return JsonResponse({"error": "Invalid symbol."}, status=400)
        task_id = str(uuid.uuid4())
        def process_task():
            try:
                cached_result = cache.get(f"news_{company_name}")
                if cached_result:
                    cache.set(f"news_status_{task_id}", {"status": "completed", "company_name": company_name}, timeout=300)
                    return
                cache.set(f"news_status_{task_id}", {"status": "processing", "company_name": company_name}, timeout=300)
                response = client.responses.parse(
                    model="gpt-4.1",
                    tools=[{"type": "web_search_preview"}],
                    input=[
                        {
                            "role": "system",
                            "content": "You are an ESG and financial news expert. Your task is to find the most relevant and recent ESG and financial news articles for a given company. Limit the results to 5 articles, ensuring they are as recent as possible and highly relevant to the company's ESG and financial performance."
                        },
                        {
                            "role": "user",
                            "content": (
                                f"Find the news articles for {company_name}.\n"
                                f"Return a structured JSON response."
                            )
                        }
                    ],
                    text_format=NewsFormat,
                )
                event: NewsFormat = response.output_parsed
                serialized_event = event.dict()
                cache.set(f"news_{company_name}", serialized_event, timeout=300)
                cache.set(f"news_status_{task_id}", {"status": "completed", "company_name": company_name}, timeout=300)
            except Exception as e:
                cache.set(f"news_status_{task_id}", {"status": "error", "message": str(e)}, timeout=300)
        Thread(target=process_task).start()
        return JsonResponse({"status": "processing", "task_id": task_id}, status=202)
    except Exception as e:
        return JsonResponse({"error": "An error occurred while generating ESG news."}, status=500)

@api_view(["GET"])
@login_required
def check_esg_news_status(request, task_id):
    status = cache.get(f"news_status_{task_id}")
    if not status:
        return JsonResponse({"status": "not_found"}, status=404)
    if status.get("status") == "completed":
        company_name = status.get("company_name")
        result = cache.get(f"news_{company_name}")
        return JsonResponse({"status": "completed", "result": result}, status=200)
    if status.get("status") == "error":
        return JsonResponse(status, status=500)
    return JsonResponse(status, status=200)

@csrf_exempt
@login_required
def fetch_esg_peer_scores(request, symbol):
    try:
        conn = http.client.HTTPSConnection("yahoo-finance-real-time1.p.rapidapi.com")
        headers = {
            'x-rapidapi-key': "c4cf9f510cmsh80ee50ea6a7d2b3p171c27jsnab5350889c90",
            'x-rapidapi-host': "yahoo-finance-real-time1.p.rapidapi.com"
        }
        conn.request("GET", f"/stock/get-similar?region=US&lang=en-US&symbol={symbol}", headers=headers)
        res = conn.getresponse()
        data = res.read()
        similar_companies = json.loads(data)
        quotes = similar_companies.get("finance", {}).get("result", {}).get("quotes", [])
        if not quotes:
            return JsonResponse({"error": "No similar companies found."}, status=404)
        peer_scores = []
        for quote in quotes:
            peer_symbol = quote.get("symbol")
            peer_name = quote.get("shortName", "Unknown")
            company = ESGCompany.objects.filter(ticker=peer_symbol).first()
            if not company:
                continue
            latest_year = get_latest_year_for_company(company)
            metrics = ESGMetric.objects.filter(company=company, year=latest_year)
            peer_scores.append({
                "ticker": peer_symbol,
                "company_name": peer_name,
                "environmental": get_metric_score(metrics, "EnvironmentPillarScore"),
                "social": get_metric_score(metrics, "SocialPillarScore"),
                "governance": get_metric_score(metrics, "GovernancePillarScore"),
                "esg": get_metric_score(metrics, "ESGScore"),
            })
        if peer_scores:
            benchmark = {
                "environmental": sum(score["environmental"] for score in peer_scores) / len(peer_scores),
                "social": sum(score["social"] for score in peer_scores) / len(peer_scores),
                "governance": sum(score["governance"] for score in peer_scores) / len(peer_scores),
                "esg": sum(score["esg"] for score in peer_scores) / len(peer_scores),
            }
        else:
            benchmark = {"environmental": 0, "social": 0, "governance": 0, "esg": 0}
        return JsonResponse({"peers": peer_scores, "benchmark": benchmark}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

class ScoreInterpretation(BaseModel):
    interpretation: str
    explanation: str

class ESGScores(BaseModel):
    Environmental: ScoreInterpretation
    Social: ScoreInterpretation
    Governance: ScoreInterpretation
    Overall: ScoreInterpretation

class Controversies(BaseModel):
    details: str
    interpretation: str

class Alignment(BaseModel):
    strategy: str
    strengths: conlist(str)
    risks: List[str]
    conclusion: str

class ESGInsight(BaseModel):
    esgScores: ESGScores
    controversies: Controversies
    alignment: Alignment
    summary: str

@api_view(["POST"])
@login_required
@csrf_exempt
def generate_ai_insight(request):
    try:
        data = request.data
        user = request.user
        company_data = data.get("companyData")
        symbol = company_data["Symbol"].strip().upper()
        if not symbol or not isinstance(symbol, str):
            return JsonResponse({"error": "Invalid symbol."}, status=400)
        if not company_data or not isinstance(company_data, dict):
            return JsonResponse({"error": "Invalid companyData."}, status=400)
        task_id = str(uuid.uuid4())
        cached_result = cache.get(f"ai_insight_{symbol}")
        if cached_result:
            return JsonResponse({"status": "completed", "result": cached_result}, status=200)
        cache.set(f"ai_insight_status_{task_id}", {"status": "processing", "symbol": symbol}, timeout=300)
        def process_task():
            try:
                preferences = UserPreferences.objects.filter(user=user).first()
                if preferences:
                    preferences = preferences.to_dict()
                if not preferences:
                    cache.set(f"ai_insight_status_{task_id}", {"status": "error", "message": "User preferences not found"}, timeout=300)
                    return
                response = client.responses.parse(
                    model="gpt-4.1-mini",
                    tools=[{"type": "web_search_preview"}],
                    input=[
                        {
                            "role": "system",
                            "content": "You are an ESG investing expert, generating analysis reports for users evaluating companies based on data and information available about the company, and the user's selected preferences."
                        },
                        {
                            "role": "user",
                            "content": (
                                f"Write an ESG analysis report about {company_data['Company Name']}. Use the given data and information about the company and user investment preferences.\n"
                                f"Company Data:\n"
                                f"{json.dumps(company_data, indent=2)}\n"
                                f"The user’s portfolio preferences are:\n"
                                f"The user’s investment strategy is: {preferences['investment_strategy']}.\n"
                                f"The user’s risk level is: {preferences['risk_level']}.\n"
                                f"The user’s ESG factor priorities are: {preferences['esg_factors']}.\n"
                                f"The user’s industry preferences are: {preferences['industry_preferences']}.\n"
                                f"The user’s industry exclusions are: {preferences['exclusions']}.\n"
                                f"The user’s report preference is: {preferences['transparency_level']}.\n"
                                f"Return a structured JSON response."
                            )
                        }
                    ],
                    text_format=ESGInsight,
                )
                event: ESGInsight = response.output_parsed
                serialized_event = event.dict()
                cache.set(f"ai_insight_{symbol}", serialized_event, timeout=300)
                cache.set(f"ai_insight_status_{task_id}", {"status": "completed", "symbol": symbol}, timeout=300)
            except Exception as e:
                cache.set(f"ai_insight_status_{task_id}", {"status": "error", "message": str(e)}, timeout=300)
        Thread(target=process_task).start()
        return JsonResponse({"status": "processing", "task_id": task_id}, status=202)
    except Exception as e:
        return JsonResponse({"error": "An error occurred while generating ESG insight."}, status=500)

@api_view(["GET"])
@login_required
def check_ai_insight_status(request, task_id):
    status = cache.get(f"ai_insight_status_{task_id}")
    if not status:
        return JsonResponse({"status": "not_found"}, status=404)
    if status.get("status") == "completed":
        symbol = status.get("symbol")
        result = cache.get(f"ai_insight_{symbol}")
        return JsonResponse({"status": "completed", "result": result}, status=200)
    if status.get("status") == "error":
        return JsonResponse(status, status=500)
    return JsonResponse(status, status=200)

def is_market_open():
    cache_key = "market_status"
    cached_status = cache.get(cache_key)
    if cached_status:
        return cached_status == "open"
    try:
        url = f'https://www.alphavantage.co/query?function=MARKET_STATUS&apikey={ALPHA_VANTAGE_API_KEY}'
        response = requests.get(url)
        data = response.json()
        us_market = next(
            (market for market in data.get("markets", []) if market["region"] == "United States"),
            None
        )
        if us_market:
            current_status = us_market["current_status"]
            cache.set(cache_key, current_status, timeout=60 * 15)
            return current_status == "open"
    except Exception as e:
        pass
    return False