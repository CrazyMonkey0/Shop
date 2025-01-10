from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('payment/', views.request_to_payment_gateway, name='request_to_payment_gateway'),
    path('paid/<int:order_id>/', views.paid_order, name='paid_order'),
    path('admin/order/<int:order_id>/', views.admin_order_detail,
         name='admin_order_detail'),
]
