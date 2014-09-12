# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from app.utils.crispymixin import *


class SubscribeForm(CrispyModelForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'email', 'phone')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if get_user_model().objects.filter(email__iexact=email):
            raise forms.ValidationError(
                u'Такой email уже зарегистрирован',
                code='email_duplicate',
            )
        return email

    def save(self, commit=True):
        user = super(SubscribeForm, self).save(commit=False)
        user.username = user.email
        user.is_active = False
        if commit:
            user.save()
        return user

    def get_layout(self, *args, **kwargs):
        self.helper.form_class = ''
        return Layout(
            'first_name',
            'email',
            'phone',
            StrictIconButton(u'Отправить', 'fa fa-share', css_class='btn btn-warning',
                             type='submit')
        )
