from django.shortcuts import render
from .models import Category, Products, Cart, Wishlist


def home(request):

    categories = Category.objects.filter(is_visible=True).order_by('sort')
    products = Products.objects.filter(is_visible=True).order_by('sort')

    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        wishlist = Wishlist.objects.get(user=request.user)
    else:
        cart = None
        wishlist = None

    context = {
        "categories": categories,
        "products": products,
        "cart": cart,
        "wishlist": wishlist,
        "book_table_form": book_table_form
    }

    return render(request, "index.html", context)


def thanks(request):
    return render(request, 'thanks.html')
