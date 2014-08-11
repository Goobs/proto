# -*- coding: UTF-8 -*-
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *


class _AbstractForm:
    """
    Abstract crispy helper form.
    """
    def get_layout(self, *args, **kwargs):
        return None

    def filter_django_kwargs(self, kwargs):
        result = {}
        # Django form accepts nothing but these arguments.
        for kwarg in kwargs.keys():
            if kwarg in ['data', 'files', 'initial', 'instance', 'prefix']:
                result[kwarg] = kwargs[kwarg]
        return result

    def init_crispy(self, args, kwargs):
        self.helper = FormHelper()

        self.helper.form_class = kwargs.pop('form_class', 'form-horizontal')
        self.helper.form_tag = kwargs.pop('form_tag', True)
        self.helper.form_action = kwargs.pop('form_action', None)
        self.helper.form_method = kwargs.pop('form_method', 'post')
        self.helper.html5_required = True

    def init_crispy_layout(self, args, kwargs):
        layout = self.get_layout(*args, **kwargs)
        if layout:
            self.helper.layout = layout


class CrispyForm(forms.Form, _AbstractForm):
    """
    Represents default crispy form with ``form-horizontal`` layout.
    To override layout you should implement ``get_layout(self, *args, **kwargs)`` method.
    """
    def __init__(self, *args, **kwargs):
        self.init_crispy(args, kwargs)
        super(CrispyForm, self).__init__(*args, **self.filter_django_kwargs(kwargs))
        self.init_crispy_layout(args, kwargs)


class CrispyModelForm(forms.ModelForm, _AbstractForm):
    """
    Represents default crispy model form with ``form-horizontal`` layout.
    To override layout you should implement ``get_layout(self, *args, **kwargs)`` method.
    """
    def __init__(self, *args, **kwargs):
        self.init_crispy(args, kwargs)
        super(CrispyModelForm, self).__init__(*args, **self.filter_django_kwargs(kwargs))
        self.init_crispy_layout(args, kwargs)


class StrictIconButton(StrictButton):
    """
    Represents StrictButton with icon before text.
    """
    def __init__(self, content, icon, **kwargs):
        content = u'<i class="%s %s"></i> %s' % (
            icon.split('-')[0], icon, content
        )
        css_class = kwargs.pop('css_class', 'btn-default')
        super(StrictIconButton, self).__init__(content, css_class=css_class, **kwargs)
