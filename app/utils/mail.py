# -*- coding: utf-8 -*-

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.models import Site


def get_site_url():
    return 'http://%s' % Site.objects.get_current().domain


def send_mail(subject, to, template, context={}, in_reply_to=None):
    """
    Renders template and sends it to recipients.
    """
    # Email should be a list or a tuple.
    if not isinstance(to, (tuple, list)):
        to = (to, )

    context['home_url'] = get_site_url()
    # Sending message through Django.
    message = EmailMessage(subject=subject.replace('\n', '').replace('\r', ''),
                           body=render_to_string(template, context),
                           to=to,)
    message.content_subtype = 'html'
    if in_reply_to:
        message.extra_headers['In-Reply-To'] = in_reply_to
    message.send()
