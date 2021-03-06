import inspect

from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import redirect_to_login, logout_then_login
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.utils.encoding import force_text
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, Http404, HttpResponse, StreamingHttpResponse


class AccessMixin(object):
    login_url = None
    raise_exception = False
    redirect_field_name = REDIRECT_FIELD_NAME  # Set by django.contrib.auth
    redirect_unauthenticated_users = False

    def get_login_url(self):
        login_url = self.login_url or settings.LOGIN_URL
        if not login_url:
            raise ImproperlyConfigured(
                'Define {0}.login_url or settings.LOGIN_URL or override '
                '{0}.get_login_url().'.format(self.__class__.__name__))

        return force_text(login_url)

    def get_redirect_field_name(self):
        if self.redirect_field_name is None:
            raise ImproperlyConfigured(
                '{0} is missing the '
                'redirect_field_name. Define {0}.redirect_field_name or '
                'override {0}.get_redirect_field_name().'.format(
                    self.__class__.__name__))
        return self.redirect_field_name

    def handle_no_permission(self, request):
        if self.raise_exception:
            if self.redirect_unauthenticated_users and not request.user.is_authenticated:
                return self.no_permissions_fail(request)
            else:
                if inspect.isclass(self.raise_exception) and issubclass(self.raise_exception, Exception):
                    raise self.raise_exception
                if callable(self.raise_exception):
                    ret = self.raise_exception(request)
                    if isinstance(ret, (HttpResponse, StreamingHttpResponse)):
                        return ret
                raise PermissionDenied

        return self.no_permissions_fail(request)

    def no_permissions_fail(self, request=None):
        """
        Called when the user has no permissions and no exception was raised.
        This should only return a valid HTTP response.
        By default we redirect to login.
        """
        return redirect_to_login(request.get_full_path(),
                                 self.get_login_url(),
                                 self.get_redirect_field_name())


class LoginRequiredMixin(AccessMixin):
    """
    View mixin which verifies that the user is authenticated.
    NOTE:
        This should be the left-most mixin of a view, except when
        combined with CsrfExemptMixin - which in that case should
        be the left-most mixin.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission(request)

        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

@method_decorator(user_passes_test(lambda user: user.is_superuser), name = 'dispatch')
class IsAdminMixin(View):
    pass