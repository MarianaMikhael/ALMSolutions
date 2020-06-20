"""
https://docs.djangoproject.com/pt-br/2.2/howto/custom-template-tags/
"""
from django import template
from datetime import datetime
from django.utils import formats

register = template.Library()


@register.simple_tag
def footer_message():
    return "TecBan SA"


@register.simple_tag(takes_context=True)
def hora_servidor(context, format_string):
    return datetime.now().strftime(format_string)
# {% load custom_tags %}
# {% hora_servidor "%Y-%m-%d %I:%M %p" as the_time %}
# {{ the_time }}
