from django.urls import path
from .import views



urlpatterns = [
    path('signup',views.register,name='signup'),
    path('login',views.user_login,name='login'),
    path('',views.home,name='home'),
    path('logout',views.user_logout,name='logout'),
    path('register_otp',views.otp_register,name='register_otp'),
    path('category/<slug:category_slug>',views.home,name='products_by_category'),
    path('search',views.search,name='search'),
    path('view_account',views.view_account,name='view_account')
]
