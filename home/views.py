from django.shortcuts import render, get_object_or_404
from product.models import Category, Products
from cart.models import Cart
from wishlist.models import Wishlist


def home(request):
    categories = Category.objects.filter(is_visible=True).order_by('sort')

    selected_category_slug = request.GET.get('category', 'all')

    if selected_category_slug == 'all':
        products = Products.objects.filter(is_visible=True).order_by('sort')
    else:
        selected_category = get_object_or_404(Category, slug=selected_category_slug)
        products = Products.objects.filter(categories=selected_category, is_visible=True).order_by('sort')

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price and max_price:
        products = products.filter(price__gte=min_price, price__lte=max_price)
    elif min_price:
        products = products.filter(price__gte=min_price)
    elif max_price:
        products = products.filter(price__lte=max_price)

    discounted_category = Category.objects.get(slug='discounted')
    discounted_products = Products.objects.filter(categories=discounted_category, is_visible=True).order_by('sort')

    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        wishlist = Wishlist.objects.get(user=request.user)
    else:
        cart = None
        wishlist = None

    context = {
        'categories': categories,
        'products': products,
        'discounted_products': discounted_products,
        'cart': cart,
        'wishlist': wishlist,
        'selected_category_slug': selected_category_slug,
        'min_price': min_price,
        'max_price': max_price,
    }

    return render(request, "index.html", context)
