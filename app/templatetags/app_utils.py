# -*- coding: utf-8 -*-

from django import template
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http.request import QueryDict

register = template.Library()


@register.simple_tag
def url_replace(request, field, value=None):
    dict_ = request.GET.copy()
    if value:
        dict_[field] = value
    else:
        del dict_[field]
    return dict_.urlencode()


@register.simple_tag
def url_create(url_name, param, field, value):
    dict_ = QueryDict('').copy()
    dict_[field] = value
    return reverse(url_name, args=[param]) + '?' + dict_.urlencode()


@register.assignment_tag()
def get_settings(setting_name):
    """
    Gets parameter from project settings:
        {% get_settings 'APP_DEFAULT_VAR' as var %}
    """
    return getattr(settings, setting_name, None)


@register.tag(name='app')
def app_installed(parser, token):
    """
    Check if app with given name installed:
        {% app 'app.plugins.app' %}
            ...
        {% elseapp %}
            ...
        {% endapp %}
    """
    tag_name, app_name = token.split_contents()
    app_name = app_name[1:-1]

    if app_name in settings.INSTALLED_APPS:
        nodelist_true = parser.parse(('elseapp', 'endapp'))
        token = parser.next_token()
        if token.contents == 'elseapp':
            parser.skip_past('endapp')
        return AppNode(nodelist_true, app_name)
    while parser.tokens:
        token = parser.next_token()
        if token.token_type == 2 and token.contents in ('elseapp', 'endapp'):
            break
    if token.contents == 'elseapp':
        nodelist_false = parser.parse(('endapp',))
        parser.delete_first_token()
    else:
        return template.TextNode('')

    return AppNode(nodelist_false, app_name)


class AppNode(template.Node):
    def __init__(self, nodelist, app_name):
        self.nodelist = nodelist
        self.app_name = app_name

    def render(self, context):
        return self.nodelist.render(context)
