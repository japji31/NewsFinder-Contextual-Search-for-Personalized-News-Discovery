from django.contrib import admin
from django.urls import path, include
from search_app import views
from api import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(urls)),

]
