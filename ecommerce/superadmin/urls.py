from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('',views.master_signin,name="admin_signin"),
    path('admin_home/',views.admin_home,name="admin_home"),
    path('customer/',views.customer,name="customer"),
    path('customer_pickoff/<customer_id>',views.customer_pickoff,name="customer_pickoff"),
    path('add_product/',views.add_product,name="add_product"),
    path('view_product/',views.view_product,name="view_product"),
    path('delete-adminprod/<int:id>',views.delete_adminprod,name="delete-adminprod"),
    path('edit_product/<str:id>/', views.edit_product,name='product_edit'),
    path('admin_logout',views.admin_logouts,name='admin_logout'),
    path('order_details',views.order_details,name='order_details'),
    path('edit_order/<int:id>',views.edit_order,name='edit_order'),
] 