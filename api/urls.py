from django.urls import path
from .views import signup_view, login_view, check_user_exists, logout_view, preferences_view, app_data, update_settings, search_company, add_stock, get_portfolio, remove_stock, get_stock_price

urlpatterns = [
    path('account/signup/', signup_view, name='signup'),
    path('account/login/', login_view, name='login'),
    path('account/check-user/', check_user_exists, name='check_user_exists'),
    path('account/logout/', logout_view, name='logout'),
    path('account/preferences/', preferences_view, name='preferences'),
    path('api/app-data', app_data, name='app_data'),
    path('account/update-settings/', update_settings, name='update_settings'),
    path('search-company/', search_company, name='search_company'),
    path('api/add-stock/', add_stock, name='add_stock'),  # Ensure this line is present
    path('api/get-portfolio/', get_portfolio, name='get_portfolio'),
    path('api/remove-stock/<int:stock_id>/', remove_stock, name='remove_stock'),
    path('api/get-stock-price/', get_stock_price, name='get_stock_price'),
]
