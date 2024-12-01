from django.contrib import messages
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from payments.models import Order
from .forms import NewUserCreationForm


def login_view(request):
    """
    Handles user login.

    Authenticates the user using the provided username and password.
    If authentication is successful, logs in the user and redirects to the home page.
    Otherwise, displays an error message.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the home page on success or renders the login page on failure.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')


def register_view(request):
    """
    Handles user registration.

    Processes the registration form and creates a new user account.
    If the form is valid, saves the user and redirects to the login page with a success message.
    Otherwise, displays form errors.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the login page on success or renders the registration page on failure.
    """
    if request.method == 'POST':
        form = NewUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = NewUserCreationForm()

    return render(request, 'register.html', {'form': form})


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