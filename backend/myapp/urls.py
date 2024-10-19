from django.urls import path
from .views import back_test, predict_data

urlpatterns = [
    path('api/backtest/', back_test, name='back_test'),
    path('api/predict-data', predict_data, name='predict_data'),
]