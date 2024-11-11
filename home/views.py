from django.shortcuts import render, get_object_or_404
from blog.models import BlogSection, BlogWindow
from product.models import Category, Products
from cart.models import Cart
from wishlist.models import Wishlist
from .models import Banner, Feature, Deal, Slider


def home(request):
    """
    Handles the rendering of the homepage with various context data such as:
    - Categories
    - Blog sections and windows
    - Features
    - Banners and promotions
    - Products (based on category filter)
    - Discounted products
    - User's cart and wishlist (if authenticated)

    Args:
        request (HttpRequest): The HTTP request object, which contains session data and user info.

    Returns:
        HttpResponse: Renders the "main.html" template with all the required context.

    Example:
        - When a user visits the homepage, the function fetches and passes all necessary data
          (products, categories, blog sections, etc.) to the template for rendering.
    """
    categories = Category.objects.filter(is_visible=True).order_by('sort')
    blog_sections = BlogSection.objects.all()[:3]
    blog_windows = BlogWindow.objects.all()
    features = Feature.objects.all()
    banners = Banner.objects.filter(is_visible=True).order_by('sort')
    selected_category_slug = request.GET.get('category', 'all')
    deal = Deal.objects.first()
    slider = Slider.objects.first()

    if selected_category_slug == 'all':
        products = Products.objects.filter(is_visible=True).order_by('sort')
    else:
        selected_category = get_object_or_404(Category, slug=selected_category_slug)
        products = Products.objects.filter(categories=selected_category, is_visible=True).order_by('sort')

    discounted_category = get_object_or_404(Category, slug='discounted')
    discounted_products = Products.objects.filter(categories=discounted_category, is_visible=True).order_by('sort')

    cart = None
    wishlist = None
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)

    context = {
        'slider': slider,
        'deal': deal,
        'blog_sections': blog_sections,
        'blog_windows': blog_windows,
        'features': features,
        'banners': banners,
        'categories': categories,
        'products': products,
        'discounted_products': discounted_products,
        'cart': cart,
        'wishlist': wishlist,
        'selected_category_slug': selected_category_slug,
    }

    return render(request, "main.html", context)
