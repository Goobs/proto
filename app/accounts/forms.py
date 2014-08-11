# -*- coding: UTF-8 -*-

from app.utils.crispymixin import *
from .models import *


class LoginForm(CrispyForm):
    username = forms.CharField(label=u'Логин', required=True)
    password = forms.CharField(label=u'Пароль', widget=forms.PasswordInput(), required=True)

    def get_layout(self, *args, **kwargs):
        self.helper.form_class = ''
        self.helper.label_class = 'sr-only'
        return Layout(
            PrependedText('username', u'<i class="fa fa-user"></i>', placeholder=u'E-mail'),
            PrependedText('password', u'<i class="fa fa-lock"></i>', placeholder=u'Пароль'),
            Div(
                StrictIconButton(
                    u'Войти', 'fa-sign-in',
                    type='submit',
                    css_class='btn-primary'
                ),
                css_class='form-group'
            )
        )


class UserRegistrationForm(CrispyModelForm):
    email = forms.EmailField(max_length=75, required=True, label=u'E-mail')
    first_name = forms.CharField(max_length=255, required=True, label=u'ФИО')
    company = forms.CharField(label=u'Компания')

    class Meta:
        model = User
        fields = ('first_name', 'email', 'password', 'password2', 'position')
        widgets = {
            'password': forms.PasswordInput,
        }

    password2 = forms.CharField(max_length=100, label=u'Подтверждение пароля', widget=forms.PasswordInput)

    error_messages = {
        'password_mismatch': u'Пароли не совпадают',
        'email_duplicate': u'Пользователь с таким E-mail уже существует',
    }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email):
            raise forms.ValidationError(
                self.error_messages['email_duplicate'],
                code='email_duplicate',
            )
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.username = user.email
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    def get_layout(self, *args, **kwargs):
        self.helper.form_tag = False
        return Layout(
            Div(
                HTML(u'<h4>Пользователь</h4>'),
                Div(
                    Div(
                        Field('first_name', placeholder=u'Иванов Иван Петрович'),
                        Field('email', placeholder=u'ivanov@example.com'),
                        css_class='col-md-6'
                    ),
                    Div(
                        Field('password'),
                        Field('password2'),
                        css_class='col-md-6'
                    ),
                    css_class='row'
                ),
                css_class=''
            ),
        )

