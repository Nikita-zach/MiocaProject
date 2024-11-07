from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def multiply(value, factor):
    return Decimal(value) * Decimal(factor)
