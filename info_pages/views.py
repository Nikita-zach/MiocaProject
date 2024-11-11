from django.shortcuts import render
from .models import ServiceSection, Stuff, Testimonials, BrandIcons, FAQ
from home.models import Feature


def about_page(request):
    """
    Renders the 'About Us' page with service, team, and testimonials content.

    - Retrieves the first instance of the `ServiceSection` model and all `Feature`, `Stuff`, `Testimonials`, and `BrandIcons` entries.
    - Passes the retrieved data into the 'about.html' template.

    Context:
        service_section (ServiceSection): The primary service information.
        features (QuerySet): List of all features.
        team (QuerySet): List of visible team members sorted by their display order.
        testimonials (QuerySet): All testimonial entries.
        brands (QuerySet): All brand icons.

    Template:
        about.html: Template for rendering the 'About Us' page.
    """
    service_section = ServiceSection.objects.first()
    features = Feature.objects.all()
    team = Stuff.objects.filter(is_visible=True).order_by('sort')
    testimonials = Testimonials.objects.all()
    brands = BrandIcons.objects.all()

    context = {
        'service_section': service_section,
        'features': features,
        'team': team,
        'testimonials': testimonials,
        'brands': brands,
    }
    return render(request, 'about.html', context)


def faq_view(request):
    """
    Renders the FAQ page, displaying a list of frequently asked questions.

    - Retrieves all instances of the `FAQ` model.
    - Passes the retrieved data into the 'faq.html' template.

    Context:
        faqs (QuerySet): All FAQ entries.

    Template:
        faq.html: Template for rendering the FAQ page.
    """
    faqs = FAQ.objects.all()
    return render(request, 'faq.html', {'faqs': faqs})


def custom_404_view(request, exception=None):
    """
    Custom view to render the 404 error page.

    - Renders a custom '404.html' template.
    - Sets HTTP response status to 404.

    Parameters:
        exception (Exception, optional): Optional exception parameter.

    Template:
        404.html: Template for rendering the 404 error page.
        :param exception:
        :param request:
    """
    return render(request, '404.html', status=404)


def privacy_policy(request):
    """
    Renders the Privacy Policy page.

    - Loads the 'privacy-policy.html' template.

    Template:
        privacy-policy.html: Template for rendering the Privacy Policy page.
    """
    return render(request, 'privacy-policy.html')



