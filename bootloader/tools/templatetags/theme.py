from django import template
from django.conf import settings
from django.template import Context, Template


register = template.Library()


@register.simple_tag
def theme(file):
    template = Template(file)
    context = Context({
        'theme': settings.DEFAULT_THEME,
    })

    return '/static/%s' % template.render(context)
