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



@register.filter
def capitalize_first(value):
    return value.title()

@register.simple_tag
def get_count(objects):
    return  objects.count()

@register.simple_tag
def view_many_to_many(objects):
    a=""
    for obj in objects :
      a+=f"* {obj.name}"
    return a

@register.inclusion_tag('dash/sidebar.html', takes_context=True)
def sidebar_tag(context, active):
    return {
        "active": active,
        "user": context["user"],
        "perms": context["perms"],
    }
