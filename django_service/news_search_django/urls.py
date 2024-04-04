from django.contrib import admin
from django.urls import path
from search_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.user_signup, name="signup"),
    path('login/', views.user_login, name="login"),
    path('news/', views.user_ml, name="news"),
    path('news_search/', views.context_search, name="context_search"),
]
