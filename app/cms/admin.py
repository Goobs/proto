# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.conf import settings

from feincms.module.page.models import Page
from feincms.module.page.admin import PageAdmin as _PageAdmin
from feincms.admin import item_editor
from treeadmin.admin import TreeAdmin
from reversion.admin import VersionAdmin


class PageAdmin(TreeAdmin, _PageAdmin, VersionAdmin):

    class Media:
        js = ('admin/inlines.js',)
        css = {'all': ('admin/feincms.css',)}

    fieldsets = [
        (None, {
            'fields': [
                ('title', 'slug'),
                ('active', 'in_navigation'),
            ],
        }),
        (_('Other options'), {
            'classes': ['grp-collapse grp-closed'],
            'fields': [
                'template_key', 'parent', 'override_url', 'redirect_to'],
        }),
        item_editor.FEINCMS_CONTENT_FIELDSET,
    ]

    list_display = ['short_title', 'active', 'in_navigation', 'template']
    list_filter = ()
    search_fields = ()

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = { 'title': u'Добавить страницу' }
        return super(PageAdmin, self).add_view(request, form_url=form_url, extra_context=extra_context)


FEINCMS_USE_PAGE_ADMIN = getattr(settings, 'FEINCMS_USE_PAGE_ADMIN', True)

if FEINCMS_USE_PAGE_ADMIN:
    admin.site.unregister(Page)
    admin.site.register(Page, PageAdmin)
