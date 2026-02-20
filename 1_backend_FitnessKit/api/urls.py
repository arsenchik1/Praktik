from django.urls import path
from .views import GetEmployeesView

urlpatterns = [
    path('team/get_employees', GetEmployeesView.as_view(), name='get_employees'),
]
