from django import template

register = template.Library()

@register.filter(name='split')
def split(value, arg):
    """
    Split a string by the given separator.
    Usage: {{ "1001,1002,1003"|split:"," }}
    """
    if value:
        return [item.strip() for item in value.split(arg) if item.strip()]
    return []

@register.filter(name='trim')
def trim(value):
    """
    Remove leading and trailing whitespace.
    Usage: {{ " 1001 "|trim }}
    """
    if value:
        return value.strip()
    return value
