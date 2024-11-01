"""
URL configuration for MiocaProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from accounts.views import login_register_view, account_dashboard
from blog.views import blog_detail, blog_list_view
from cart.views import remove_from_cart
from compare.views import product_compare_view, add_to_compare, remove_from_compare
from home import views
from payments.views import checkout_view, thank_you_view
from product.views import product_detail_view, shop_view, add_to_cart
from info_pages.views import faq_view, custom_404_view, privacy_policy, about_page
from wishlist.views import remove_from_wishlist, add_to_wishlist

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('product/<int:product_id>/', product_detail_view, name='product_detail'),
    path('shop/', shop_view, name='shop'),
    path('blog/<int:blog_id>/', blog_detail, name='blog_detail'),
    path('blogs/<int:blog_window_id>/', blog_list_view, name='blog_list'),
    path('compare/', product_compare_view, name='product_compare'),
    path('login/', login_register_view, name='login_register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login_register'), name='logout'),
    path('checkout/', checkout_view, name='checkout'),
    path('thank-you/', thank_you_view, name='thank_you'),
    path('account/', account_dashboard, name='account_dashboard'),
    path('faq/', faq_view, name='faq'),
    path('privacy-policy/', privacy_policy, name='privacy_policy'),
    path('about/', about_page, name='about'),
    path('remove-from-cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('add-to-wishlist/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:product_id>/', remove_from_wishlist, name='remove_from_wishlist'),
    path('add-to-compare/<int:product_id>/', add_to_compare, name='add_to_compare'),
    path('remove-from-compare/<int:product_id>/', remove_from_compare, name='remove_from_compare'),

]
handler404 = custom_404_view
