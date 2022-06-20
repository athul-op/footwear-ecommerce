from . import views
from django.urls import path




urlpatterns = [
    path('category/product/<slug:slug>/',views.product_details,name="product"),
    path('about',views.about,name='about')
    
    
]

