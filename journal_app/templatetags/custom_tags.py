from django import template

register = template.Library()

@register.filter(name='has_hidden_attr')
def has_hidden_attr(field):
    return field.field.widget.attrs.get('hidden', False)
