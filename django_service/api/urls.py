from django.urls import path
from search_app import views

urlpatterns = [
    path('signup/', views.user_signup, name="signup"),
    path('login/', views.user_login, name="login"),
    path('news/', views.user_ml, name="user_ml"),
]