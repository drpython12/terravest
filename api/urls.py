from django.urls import path
from .views import signup_view, login_view, check_user_exists, logout_view, preferences_view

urlpatterns = [
    path('account/signup/', signup_view, name='signup'),  # URL for the signup view
    path('account/login/', login_view, name='login'),     # URL for the login view
    path('account/check-user/', check_user_exists, name='check_user_exists'),  # URL for the logout view
    path('account/logout/', logout_view, name='logout'),  # URL for the logout view
    path('account/preferences/', preferences_view, name='preferences'),  # URL for the preferences view
]
