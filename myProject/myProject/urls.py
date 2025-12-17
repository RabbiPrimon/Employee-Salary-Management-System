from django.contrib import admin
from django.urls import path, include
from myApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include('myApp.urls')),
   
    
]
