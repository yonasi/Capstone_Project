from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('login/', views.UserLoginView.as_view(), name='user-login'),
    path('profile/', views.user_profile_view, name='user-profile'),
    path('profile/update/', views.user_profile_view, name='profile-update'),
    path('password/change/', views.PasswordChangeView.as_view(), name='password-change'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]