from django.urls import path
from . import views

urlpatterns = [
path('',views.store,name='store'),
path('cart/',views.cart,name='cart'),
path('checkout/',views.checkout,name='checkout'),
path('main/',views.main,name='main'),
path('update_item/',views.updateItem,name='update_item'),
path('process_order/',views.processOrder,name='process_order'),
path('register/',views.Register,name='register'),
path('login/',views.Login,name='login'),
path('logout/',views.Logout,name='logout'),
path('search/',views.Search,name='search'),


]
