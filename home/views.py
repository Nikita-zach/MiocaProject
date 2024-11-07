from django.shortcuts import render, get_object_or_404
from blog.models import BlogSection, BlogWindow
from product.models import Category, Products
from cart.models import Cart
from wishlist.models import Wishlist
from .models import NewsletterSubscriber, Banner, Feature, Deal, Slider
from .forms import NewsletterForm

def home(request):
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

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    discounted_category = get_object_or_404(Category, slug='discounted')
    discounted_products = Products.objects.filter(categories=discounted_category, is_visible=True).order_by('sort')

    cart = None
    wishlist = None
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)

    context = {
        'slider': slider,
        'deal':deal,
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
        'min_price': min_price,
        'max_price': max_price,
    }

    return render(request, "main.html", context)


def subscribe_newsletter(request):
    message = None
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            if not NewsletterSubscriber.objects.filter(email=email).exists():
                form.save()
                message = "Thank you! You have successfully subscribed to the newsletter."
            else:
                message = "You are already subscribed to our newsletter."
        else:
            message = "Please enter a valid email address."
    else:
        form = NewsletterForm()

    current_path = request.path

    return render(request, current_path, {'form': form, 'message': message})