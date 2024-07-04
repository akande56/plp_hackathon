from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "archpragmatic_vtu.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import archpragmatic_vtu.users.signals  # noqa: F401
        except ImportError:
            pass
