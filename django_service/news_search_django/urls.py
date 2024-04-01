from django.contrib import admin
from django.urls import path
from search_app import views

urlpatterns = [
    path('news_search/', views.context_search,name="context_search"),
    path('admin/', admin.site.urls),
]
