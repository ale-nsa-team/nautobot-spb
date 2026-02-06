# nautobot_spb/__init__.py
#from .plugin import NautobotSPBConfig

# Nautobot expects a "config" variable exposed at package level
#config = NautobotSPBConfig

# nautobot_spb/__init__.py
# nautobot_spb/__init__.py
from nautobot.apps import NautobotAppConfig


class NautobotSPBConfig(NautobotAppConfig):
    """Nautobot SPB Plugin Configuration."""

    name = "nautobot_spb"
    label = "nautobot_spb"
    verbose_name = "Nautobot SPB"
    version = "0.1"
    min_version = "2.4.0"
    description = "Plugin SPB pour Nautobot (Shortest Path Bridging)"
    author = "Lina"
    author_email = "linaouali547@gmail.com"

    base_url = "spb"
    required_settings = []
    default_settings = {}
    caching_config = {}

    navigation = "nautobot_spb.navigation"
    app_extensions = ["nautobot_spb.extend"]
    urlpatterns = "nautobot_spb.urls"

    def ready(self):
        """Called when Nautobot starts and the plugin is loaded."""
        super().ready()
        from . import admin  # noqa
        from . import registration
        #from . import signals
        registration.register_spb_models_for_features()


config = NautobotSPBConfig
