from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogWindow, BlogSection, Comment


def blog_detail(request, blog_id):
    """
    Displays the details of a specific blog section and allows users to add comments.

    This view retrieves a `BlogSection` based on the provided `blog_id` and renders
    it with a form to submit comments. If the request is a POST, a new comment is
    created and associated with the blog section. Afterward, the user is redirected
    back to the blog detail page.

    Args:
        request (HttpRequest): The HTTP request object.
        blog_id (int): The ID of the blog section to display.

    Returns:
        HttpResponse: Renders the "blog-single.html" template with the blog section and its content.

    Example:
        A user visits a blog post, submits a comment, and is redirected back to the post page.
    """
    blog_section = BlogSection.objects.get(id=blog_id)

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        Comment.objects.create(blog_section=blog_section, name=name, email=email, message=message)
        return redirect('blog_detail', blog_section_id=blog_section.id)

    context = {
        'blog_section': blog_section,
    }
    return render(request, 'blog-single.html', context)


def blog_list_view(request, blog_window_id):
    """
    Displays a list of blog sections within a specific blog window.

    The view retrieves a `BlogWindow` based on the provided `blog_window_id` and
    renders the list of blog sections associated with this window.

    Args:
        request (HttpRequest): The HTTP request object.
        blog_window_id (int): The ID of the blog window to display.

    Returns:
        HttpResponse: Renders the "blog-search.html" template with the blog window content.

    Example:
        A user navigates to a blog window and sees all the blog sections related to it.
    """
    blog_window = get_object_or_404(BlogWindow, id=blog_window_id)

    context = {
        'blog_window': blog_window,
    }

    return render(request, 'blog-search.html', context)

def add_comment(request, blog_id):
    if request.method == "POST":
        blog_section = get_object_or_404(BlogSection, id=blog_id)
        name = request.POST.get('name')
        message = request.POST.get('message')

        comment = Comment(blog_section=blog_section, name=name, message=message)
        comment.save()

        return redirect('blog_detail', blog_id=blog_id)

    return HttpResponse(status=400)
