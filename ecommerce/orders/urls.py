from . import views
from django.urls import path




urlpatterns = [
    path('place_order/',views.place_order,name='place_order'),
    path('payments/',views.payments,name='payments'),
    path('payment_status/<int:order_number>',views.payment_status,name='payment_status'),
    path('cash-on-delivery/', views.cash_on_delivery, name='cash-on-delivery'),
    
]
