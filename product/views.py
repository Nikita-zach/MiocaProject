from decimal import Decimal, InvalidOperation
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ReviewForm
from .models import Products, Category, ProductImage, Review
from django.db.models import Avg, Count


def shop_view(request):
    """
    Displays the shop page with available products and categories.

    - Retrieves all visible categories and applies filters based on selected category, minimum price, and maximum price.
    - Calculates and annotates average rating and review count for each product.

    Context:
        categories (QuerySet): Visible categories, ordered by 'sort'.
        products (QuerySet): Filtered and sorted products.
        selected_category_slug (str): The slug of the selected category.
        min_price (Decimal): Minimum price filter.
        max_price (Decimal): Maximum price filter.

    Template:
        shop.html: Template for rendering the shop page.
    """
    categories = Category.objects.filter(is_visible=True).order_by('sort')

    selected_category_slug = request.GET.get('category', 'all')

    min_price = request.GET.get('min_price', '0')
    max_price = request.GET.get('max_price', '9999')

    products_query = Products.objects.filter(is_visible=True)

    if selected_category_slug != 'all':
        products_query = products_query.filter(categories__slug=selected_category_slug)

    try:
        min_price = Decimal(min_price) if min_price else Decimal('0')
        products_query = products_query.filter(price__gte=min_price)
    except InvalidOperation:
        min_price = Decimal('0')

    try:
        max_price = Decimal(max_price)
        products_query = products_query.filter(price__lte=max_price)
    except InvalidOperation:
        max_price = Decimal('9999')
    products = products_query.annotate(
        average_rating=Avg('reviews__rating'),
        reviews_count=Count('reviews')
    ).distinct().order_by('sort')

    context = {
        'categories': categories,
        'products': products,
        'selected_category_slug': selected_category_slug,
        'min_price': min_price,
        'max_price': max_price,
    }

    return render(request, 'shop.html', context)


def product_detail_view(request, product_id):
    """
    Displays the product detail page for a specific product.

    - Shows the selected product's details, associated images, and related products.
    - Calculates the average rating and final price.
    - Handles review form submission if POST request is received.

    Context:
        product (Products): The specific product being viewed.
        images (QuerySet): Additional images of the product.
        categories (QuerySet): Categories associated with the product.
        related_products (QuerySet): Related products in the same categories, excluding the current product.
        average_rating (float): Average rating of the product.
        final_price (Decimal): Final price after any applicable discount.
        discount_price (bool): Whether a discount price is available.
        reviews (QuerySet): Reviews for the product.
        review_count (int): Number of reviews for the product.
        review_form (ReviewForm): Form for submitting a review.

    Template:
        single-product.html: Template for rendering the product detail page.
    """
    product = get_object_or_404(Products, id=product_id)
    images = ProductImage.objects.filter(product=product)
    categories = product.categories.all()
    related_products = Products.objects.filter(
        categories__in=categories,
        is_visible=True
    ).exclude(id=product.id).distinct()[:4]

    reviews = Review.objects.filter(product=product)
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] if reviews.exists() else 0
    review_count = reviews.count()

    final_price = product.discount_price if product.discount_price else product.price
    discount_price = product.discount_price is not None

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been submitted successfully.')
            return redirect('product_detail', product_id=product.id)
        else:
            messages.error(request, 'There was an error with your review. Please try again.')

    else:
        review_form = ReviewForm()

    context = {
        'product': product,
        'images': images,
        'categories': categories,
        'related_products': related_products,
        'average_rating': average_rating,
        'final_price': final_price,
        'discount_price': discount_price,
        'reviews': reviews,
        'review_count': review_count,
        'review_form': review_form,
    }

    return render(request, 'single-product.html', context)

