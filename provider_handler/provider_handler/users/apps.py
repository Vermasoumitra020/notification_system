from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "provider_handler.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import provider_handler.users.signals  # noqa F401
        except ImportError:
            pass
