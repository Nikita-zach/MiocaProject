from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def multiply(value, factor):
    """
    Multiplies a value by a given factor. This custom template filter can be used in templates to perform
    multiplication on a value.

    Args:
        value (Decimal or numeric): The value to multiply.
        factor (numeric): The factor by which to multiply the value.

    Returns:
        Decimal: The result of multiplying `value` by `factor`.

    Example:
        {{ price|multiply:quantity }}  # Will multiply the price by the quantity in the template.
    """
    return Decimal(value) * Decimal(factor)
