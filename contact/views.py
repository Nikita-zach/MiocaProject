from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm


def contact_view(request):
    """
    Handles the rendering of the contact page and processes the contact form submission.

    - If the request method is POST, it validates the form and, if valid, saves the form and redirects the user back to the contact page.
    - If the request method is GET (or if there is no form submission), it displays the contact form.

    Args:
        request (HttpRequest): The HTTP request object, which contains the form data if the user has submitted the form.

    Returns:
        HttpResponse: Renders the "contact.html" template with the contact form for GET requests.
                      If the form is successfully submitted (POST), redirects to the contact page with a success message.

    Example:
        A user submits a contact form, and the message is saved, then the user is redirected to the contact page with a success message.
    """
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you! Your message has been sent.")
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})
