from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from cart.models import Cart
from .forms import ShippingForm, OrderForm
from .models import Order, ThankYouImage


@login_required
def checkout_view(request):
    """
    Renders the checkout page with order details and forms for user input.

    - Retrieves the user's cart and calculates the total price and shipping cost.
    - Passes cart items, total price, shipping cost, and forms for user completion.

    Context:
        cart_items (QuerySet): All items in the user's cart.
        total_price (Decimal): Total price of items in the cart.
        shipping_cost (Decimal): Shipping cost based on the cart total.
        final_total_price (Decimal): Sum of total price and shipping cost.
        shipping_form (ShippingForm): Form to input shipping details.
        order_form (OrderForm): Form to capture additional order details.

    Template:
        checkout.html: Template for rendering the checkout page.
    """
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.items.all()
    total_price = sum(item.total_price() for item in cart_items)

    shipping_cost = Decimal(0) if total_price >= Decimal(39) else Decimal(9.00)
    final_total_price = total_price + shipping_cost

    shipping_form = ShippingForm()
    order_form = OrderForm()

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'shipping_cost': shipping_cost,
        'final_total_price': final_total_price,
        'shipping_form': shipping_form,
        'order_form': order_form
    })


@login_required
def place_order(request):
    """
    Processes the placement of an order.

    - Validates shipping and order forms submitted by the user.
    - If forms are valid, creates an order with a unique number, status as 'Pending',
      and saves the total quantity and price.
    - Empties the user's cart upon successful order creation.

    Redirects:
        Success: Redirects to 'thank_you' page with a success message.
        Error: Redirects back to 'checkout' page with error messages.

    Messages:
        success: Order placed successfully.
        error: Informs the user of any form errors.

    Template:
        checkout.html: Redirects back to this template if forms are invalid.
    """
    if request.method == 'POST':
        shipping_form = ShippingForm(request.POST)
        order_form = OrderForm(request.POST)
        if shipping_form.is_valid() and order_form.is_valid():
            cart = Cart.objects.get(user=request.user)
            cart_items = cart.items.all()
            total_price = Decimal(sum(item.total_price() for item in cart_items))
            shipping_cost = Decimal(0) if total_price >= Decimal(39) else Decimal(9.00)
            final_total_price = total_price + shipping_cost

            Order.objects.create(
                user=request.user,
                status='PENDING',
                total_quantity=sum(item.quantity for item in cart_items),
                total_price=final_total_price
            )

            cart.items.all().delete()

            messages.success(request, "Your order has been placed successfully!")
            return redirect('thank_you')

        else:
            messages.error(request, "Please correct the errors in the form.")
            return redirect('checkout')

    return redirect('checkout')


def thank_you_view(request):
    """
    Renders the 'Thank You' page after an order is successfully placed.

    - Displays an image and optional content to thank the user for their purchase.

    Context:
        thank_you (ThankYouImage): The image displayed on the 'Thank You' page.

    Template:
        thank-you-page.html: Template for rendering the 'Thank You' page.
    """
    thank_you = ThankYouImage.objects.first()
    return render(request, 'thank-you-page.html',{'thank_you':thank_you})