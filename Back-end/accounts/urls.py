from django.urls import path, include
from .views import CustomRegisterView, user_info, CustomUserDetailsView, user_delete
from dj_rest_auth.views import PasswordChangeView

urlpatterns = [
    path('signup/', CustomRegisterView.as_view(), name='account_signup'),
    path('', include('dj_rest_auth.urls')),
    path('user_info/',user_info,name="user_info"),
    path('user/', CustomUserDetailsView.as_view(), name='account_userinfo'),
    path('changepassword/', PasswordChangeView.as_view(), name='rest_password_change'),
    path('delete/', user_delete, name='user_delete'),
]