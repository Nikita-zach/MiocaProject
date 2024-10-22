from django.shortcuts import render
from .models import Category, Products, Cart, Wishlist


def home(request):

    categories = Category.objects.filter(is_visible=True).order_by('sort')
    products = Products.objects.filter(is_visible=True).order_by('sort')
    discounted_category = Category.objects.get(slug='discounted')
    discounted_products = Products.objects.filter(category=discounted_category, is_visible=True).order_by('sort')

    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        wishlist = Wishlist.objects.get(user=request.user)
    else:
        cart = None
        wishlist = None

    context = {
        'discounted_products': discounted_products,
        "categories": categories,
        "products": products,
        "cart": cart,
        "wishlist": wishlist,
    }

    return render(request, "index.html", context)


def thanks(request):
    return render(request, 'thanks.html')
