# -*- coding: UTF-8 -*-

from app.utils.crispymixin import *
from django.contrib.auth.forms import *
from django.forms import ValidationError
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
                HTML(u'<a href="{% url \'password_reset\' %}" class="btn-link btn">Забыли пароль?</a>'),
                css_class='form-group'
            )
        )


class UserRegistrationForm(CrispyModelForm):
    email = forms.EmailField(max_length=75, required=True, label=u'E-mail')
    first_name = forms.CharField(max_length=255, required=True, label=u'ФИО')

    class Meta:
        model = User
        fields = ('first_name', 'email', 'password', 'password2')
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
                Div(
                    StrictIconButton(
                        u'Регистрация', 'fa-sign-in',
                        type='submit',
                        css_class='btn-primary'
                    ),
                    HTML(u'<a href="{% url \'password_reset\' %}" class="btn-link btn">Забыли пароль?</a>'),
                    css_class='form-group'
                ),
                css_class=''
            ),
        )


def user_exists_validator(email):
    from app.accounts.models import User
    if User.objects.filter(email=email):
        return email
    else:
        raise ValidationError(u'Пользователь с таким e-mail не найден в системе')


class PasswordResetForm(PasswordResetForm, CrispyForm):
    email = forms.EmailField(label=u'E-mail:', validators=[user_exists_validator])

    def get_layout(self, *args, **kwargs):
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        return Layout(
            'email',
            Div(
                Div(
                    StrictIconButton(u'Восстановить', '', type='submit', css_class='btn-primary'),
                    css_class='controls col-md-9 col-md-offset-3'
                ),
                css_class='form-group'
            ),
        )

    def save(self, domain_override=None,
             subject_template_name=None,
             email_template_name=None,
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        email = self.cleaned_data["email"]
        user = User.objects.filter(
            email__iexact=email, is_active=True).first()

        # Make sure that no email is sent to a user that actually has
        # a password marked as unusable
        if not user or not user.has_usable_password():
            return
        # c = {
        #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        #     'user': user,
        #     'token': token_generator.make_token(user),
        # }
        # send_password_reset_mail(**c)


class SetPasswordForm(SetPasswordForm, CrispyForm):

    def get_layout(self, *args, **kwargs):
        self.helper.form_class = ''
        return Layout(
            'new_password1',
            'new_password2',
            StrictIconButton(u'Отправить', '', type='submit', css_class='btn-primary'),
        )


class UserChangePasswordForm(CrispyForm):
    password = forms.CharField(label=u'Текущий', widget=forms.PasswordInput, max_length=100)
    new_password = forms.CharField(label=u'Новый', widget=forms.PasswordInput, max_length=100)
    new_confirm_password = forms.CharField(label=u'Повтор', widget=forms.PasswordInput, max_length=100)

    error_messages = {
        'password_mismatch': u'Пароли не совпадают',
    }

    def get_layout(self, *args, **kwargs):
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        return Layout(
            'password',
            'new_password',
            'new_confirm_password',
            Div(
                Div(
                    StrictIconButton(u'Сохранить', 'fa-save', type='submit', css_class='btn-primary'),
                    HTML(u'<a href="{% url \'dashboard\' %}" class="btn-link btn">Отменить</a>'),
                    css_class='col-md-offset-3 col-md-9'
                ),
                css_class='form-group'
            )
        )

    def clean_new_confirm_password(self):
        password1 = self.cleaned_data.get("new_password")
        password2 = self.cleaned_data.get("new_confirm_password")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2
