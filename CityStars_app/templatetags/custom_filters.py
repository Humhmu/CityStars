from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def to(x, y):
    try:
        return range(x, y + 1)
    except:
        return []
