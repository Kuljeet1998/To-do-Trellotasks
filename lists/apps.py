from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class ListsConfig(AppConfig):
    name = 'lists'
    # verbose_name = _('profiles')

    def ready(self):
        import lists.signals 
