from django import template

register = template.Library()

@register.filter
def attr(obj, attr_name):
    try:
        value = getattr(obj, attr_name)
        if callable(value):
            return value()
        return value
    except Exception:
        return ""
