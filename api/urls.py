from django.urls import path
from .views import (
    signup_view,
    login_view,
    check_user_exists,
    logout_view,
    preferences_view,
    app_data,
    update_settings,
    search_company,
    add_stock,
    get_portfolio,
    remove_stock,
    get_stock_price,
    get_esg_data,
    get_dashboard_data,
    chatgpt_advisor,
    get_company_esg_data,
    fetch_esg_news,
    fetch_esg_peer_scores,
    generate_ai_insight
)

urlpatterns = [
    path('api/account/signup/', signup_view, name='signup'),
    path('api/account/login/', login_view, name='login'),
    path('api/account/check-user/', check_user_exists, name='check_user_exists'),
    path('api/account/logout/', logout_view, name='logout'),
    path('api/account/preferences/', preferences_view, name='preferences'),
    path('api/app-data', app_data, name='app_data'),
    path('api/account/update-settings/', update_settings, name='update_settings'),
    path('api/search-company/', search_company, name='search_company'),
    path('api/add-stock/', add_stock, name='add_stock'),
    path('api/get-portfolio/', get_portfolio, name='get_portfolio'),
    path('api/remove-stock/<int:stock_id>/', remove_stock, name='remove_stock'),
    path('api/get-stock-price/', get_stock_price, name='get_stock_price'),
    path('api/get-esg-data/', get_esg_data, name='get_esg_data'),
    path('api/dashboard/', get_dashboard_data, name='dashboard'),
    path('api/chatgpt-advisor/', chatgpt_advisor, name='chatgpt_advisor'),  # New endpoint for ChatGPT
    path('api/get-esg-data/<str:ticker>/', get_company_esg_data, name='company_esg_data'),  # New endpoint for ChatGPT with question
    path('api/fetch-esg-news/', fetch_esg_news, name='fetch_esg_news'),
    path('api/fetch-esg-peer-scores/<str:symbol>/', fetch_esg_peer_scores, name='fetch_esg_peer_scores'),
    path('api/generate-esg-insight/', generate_ai_insight, name='generate_ai_insight'),
]
