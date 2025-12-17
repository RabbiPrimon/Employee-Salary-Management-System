from django.urls import path
from .views import add_employee, salary_report

urlpatterns = [
    path('form/', add_employee, name='form'),
    path('', salary_report, name='table'), 
]
