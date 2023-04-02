from django import template
from base64 import b64encode

register = template.Library()

@register.filter
def base64(value):
    return b64encode(value).decode('utf-8')