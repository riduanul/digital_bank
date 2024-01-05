from django.urls import path
from . import views
urlpatterns = [
    path('register', views.UserRegistrationView.as_view(), name = 'register'),
    path('login', views.UserLoginView.as_view(), name = 'login'),
    path('logout', views.UserLogoutView.as_view(), name = 'logout'),
    path('profile', views.UserProfileUpdateView.as_view(), name = 'profile'),
    path('profile/update_password', views.password_change, name = 'update_password'),
]
