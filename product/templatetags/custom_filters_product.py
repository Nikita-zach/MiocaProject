from django import template

register = template.Library()

@register.filter
def multiply(value, factor):
    return float(value) * factor


@register.filter
def range_filter(start, end):
    return range(start, end + 1)

