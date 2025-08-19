from django import template

register = template.Library()


@register.filter
def percentage(value, decimals=0):
    """
    Convert float number to percentage string
    """
    try:
        formatted_value = f"{value * 100:.{decimals}f}%"
        return formatted_value
    except (ValueError, TypeError):
        return "Invalid input"
