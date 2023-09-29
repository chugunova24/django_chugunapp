from django import template
register = template.Library()


@register.filter(name="get")
def get(indexable, i):
    print(i-1)
    return indexable[i-1]