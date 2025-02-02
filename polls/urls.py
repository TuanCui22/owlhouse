from django.urls import path
from . import views
from .views import forgot_pass_view, homepage_view, login_view, register_view, cart_view, logout_view, product_detail, listbooks_view, add_cart

app_name = 'polls'

urlpatterns = [
    path('', homepage_view, name='homepage'),
    path('forgot-password/', forgot_pass_view, name='forgot_password'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('shopping-cart/', cart_view, name='cart'),
    path('logout/', logout_view, name='logout'),
    path('item/<slug:slug>', product_detail, name='product_detail'),
    path('category/<slug:category_slug>', views.category_list, name='category_list'),
    path('search/', views.search, name='search'),
    path('lisbooks/', listbooks_view, name='listbooks'),
    path('add_cart/<int:product_id>', add_cart, name='add_cart'),
    path('account/', views.account_view, name='account'),
    path('payment', views.payment_view, name='payment')
]