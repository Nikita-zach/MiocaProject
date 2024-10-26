from django import template

register = template.Library()

@register.filter
def multiply(value, factor):
    return float(value) * factor
