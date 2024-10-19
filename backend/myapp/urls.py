from django.urls import path
from .views import back_test

urlpatterns = [
    path('api/backtest/', back_test, name='back_test'),
]