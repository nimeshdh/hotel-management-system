from django import template
from django.template.defaultfilters import floatformat

register = template.Library()

@register.filter(name='nepali_currency')
def nepali_currency(value):
    """
    Format a number as Nepali currency (₨) with proper formatting.
    
    Example: 1234.56 becomes ₨ 1,234.56
    """
    if value is None:
        return ''
    
    # Format with commas as thousand separators and 2 decimal places
    formatted_value = floatformat(value, 2)
    
    # Add commas for thousands
    parts = formatted_value.split('.')
    integer_part = parts[0]
    
    # Format with Nepali thousands separator (same as international, but for clarity)
    result = ""
    for i, char in enumerate(reversed(integer_part)):
        if i > 0 and i % 3 == 0:
            result = "," + result
        result = char + result
    
    # Add decimal part if it exists
    if len(parts) > 1:
        result = f"{result}.{parts[1]}"
    
    # Add Nepali Rupee symbol
    return f"₨ {result}"