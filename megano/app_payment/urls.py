from django.urls import path

from .views import payment, OrderPayment

urlpatterns = [
    path('new/', payment, name='pay_new'),
    path('pay/<int:pk>/', OrderPayment.as_view(), name='pay'),
]
