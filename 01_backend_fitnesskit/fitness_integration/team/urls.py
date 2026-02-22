from django.urls import path
from .views import GetEmployeesView

urlpatterns = [
    path('get_employees/', GetEmployeesView.as_view(), name='get-employees'),
]