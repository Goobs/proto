from django.conf.urls import patterns, url
from app.utils.auth import *
from .views import *


urlpatterns = patterns('',
    url(r'^login/$', unauthorized_only(LoginView.as_view()), name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),

    # Password reset-related views.
    url(r'^accounts/reset_password/$', unauthorized_only(password_reset_view),
        name='password_reset'),
    url(r'^accounts/reset_password_done/$', unauthorized_only(PasswordResetDoneView.as_view()),
        name='password_reset_done'),
    url(r'^accounts/reset_password_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        unauthorized_only(password_reset_confirm_view),
        name='password_reset_confirm'),
    url(r'^accounts/reset_password_complete/', unauthorized_only(PasswordResetCompleteView.as_view()),
        name='password_reset_complete'),

    # Password change form.
    url(r'^accounts/change_password/?$', login_required(UserChangePasswordView.as_view()),
        name='password_change'),

    # Registration
    url(r'^registration/?$', unauthorized_only(RegistrationView.as_view()),
        name='registration'),
)
