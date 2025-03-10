from django.urls import path
from .views import signup_view, login_view, check_user_exists, logout_view, preferences_view, app_data, update_settings, search_company

urlpatterns = [
    path('account/signup/', signup_view, name='signup'),
    path('account/login/', login_view, name='login'),
    path('account/check-user/', check_user_exists, name='check_user_exists'),
    path('account/logout/', logout_view, name='logout'),
    path('account/preferences/', preferences_view, name='preferences'),
    path('api/app-data', app_data, name='app_data'),
    path('account/update-settings/', update_settings, name='update_settings'),
    path('search-company/', search_company, name='search_company'),
]
