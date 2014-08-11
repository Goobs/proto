from django.contrib.auth.decorators import *


def unauthorized_only(view_func):
    """
    Allows only unauthorized access, otherwise redirecting to root.
    """
    def is_anonymous(user):
        return user.is_anonymous()

    return user_passes_test(is_anonymous, login_url='/', redirect_field_name=None)(view_func)


def superuser_required(view_func):
    """
    Allows only super user, otherwise redirecting to root
    """
    return user_passes_test(lambda u: u.is_superuser, login_url='/', redirect_field_name=None)(view_func)
