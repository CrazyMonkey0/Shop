from django.urls import path, include
from .views import PaidApiView

app_name = 'api'


urlpatterns = [
    path('paid/', PaidApiView.as_view(), name='paid'),
]