from django.contrib import messages
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from payments.models import Order
from .forms import NewUserCreationForm


def login_register_view(request):
    """
    Handles both user login and registration in a single view.

    If the request method is POST, the function checks whether the user is attempting
    to log in or register. For login, it authenticates the user using the provided
    username and password. Upon successful login, the user is redirected to the home page
    with a success message. If authentication fails, an error message is displayed.
    For registration, a form is validated, and upon successful registration,
    the user is redirected back to the login page with a success message.
    If there are form errors, an error message is shown.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the home page after successful login,
                       or the login_register page after successful registration.
                       Renders the login page with appropriate form and messages.

    Example:
        A user submits a POST request with valid login credentials.
        The user is authenticated, logged in, and redirected to the home page.
    """
    if request.method == 'POST':
        if 'login' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")

        elif 'register' in request.POST:
            form = NewUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                messages.success(request, "Registration successful! You can now log in.")
                return redirect('login_register')
            else:
                messages.error(request, "Please correct the errors below.")
    else:
        form = NewUserCreationForm()

    return render(request, 'login.html', {
        'login_form': None,
        'register_form': form,
        'messages': messages.get_messages(request),
    })


@login_required
def account_dashboard(request):
    """
    Displays the user's account dashboard, showing their orders.

    The view requires the user to be authenticated. It retrieves all orders associated
    with the currently logged-in user and passes them to the template for rendering.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the "my-account.html" template with the user's orders.

    Example:
        After login, a user navigates to the account dashboard and sees all their past orders.
    """
    orders = Order.objects.filter(user=request.user)
    context = {
        'orders': orders,
        'user': request.user,
    }
    return render(request, 'my-account.html', context)

def logout(request):
    """
    Logs out the currently authenticated user and redirects them to the home page.

    The function calls `auth_logout()` to log out the user and clears the session data.
    Afterward, the user is redirected to the home page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects the user to the home page.

    Example:
        A user clicks the logout button and is logged out, with the session being cleared.
    """
    auth_logout(request)
    return redirect('home')