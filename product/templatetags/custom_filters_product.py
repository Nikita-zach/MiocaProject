from django import template

register = template.Library()

@register.filter
def multiply(value, factor):
    return float(value) * factor

@register.filter
def range_filter(start, end):
    return range(start, end)


@register.filter
def rating_stars(rating):
    full_stars = 'fa fa-star' * rating
    empty_stars = 'fa fa-star-o' * (5 - rating)
    return full_stars + empty_stars
