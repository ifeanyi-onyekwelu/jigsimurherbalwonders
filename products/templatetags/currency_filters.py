from django import template
from decimal import Decimal

register = template.Library()


@register.filter
def currency(value):
    """
    Format a number as Nigerian Naira currency with comma separators.
    Usage: {{ price|currency }}
    Output: ₦1,234.99
    """
    if value is None:
        return "₦0.00"

    try:
        # Convert to Decimal for precise formatting
        if isinstance(value, str):
            value = Decimal(value)
        elif not isinstance(value, Decimal):
            value = Decimal(str(value))

        # Format with comma separators and 2 decimal places
        formatted = "₦{:,}".format(value)
        return formatted
    except (ValueError, TypeError):
        return "₦0.00"


@register.filter
def currency_no_decimal(value):
    """
    Format a number as Nigerian Naira currency with comma separators but no decimals if .00
    Usage: {{ price|currency_no_decimal }}
    Output: ₦1,234 or ₦1,234.50
    """
    if value is None:
        return "₦0"

    try:
        # Convert to Decimal for precise formatting
        if isinstance(value, str):
            value = Decimal(value)
        elif not isinstance(value, Decimal):
            value = Decimal(str(value))

        # Check if the value has no decimal part
        if value % 1 == 0:
            formatted = "₦{:,}".format(int(value))
        else:
            formatted = "₦{:,}".format(value)

        return formatted
    except (ValueError, TypeError):
        return "₦0"
