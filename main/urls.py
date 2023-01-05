from django.urls import path
from main import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/<str:category>/', views.product, name='product'),
    path('prodetail/<str:id>/', views.prodetail, name='prodetail'),
    path('find/', views.find, name='find'),
    path('cart/',views.cart,name='cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('update_item/',views.updateItem,name='update_item'),  
    path('process_order/',views.processOrder,name='process_order'),
    path('confirmOrder/',views.confirmOrder,name='confirmOrder'),
    path('sell/',views.sell,name='sell'),
]