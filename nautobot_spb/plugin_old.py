# nautobot_spb/plugin.py
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

    # Important: declare navigation and URLs directly
    navigation = "nautobot_spb.navigation"
    urlpatterns = "nautobot_spb.urls"
    app_extensions = ["nautobot_spb.extend"]

    def ready(self):
        """Called when Nautobot starts and plugin is loaded."""
        from . import admin  # noqa


# This is what Nautobot looks for
config = NautobotSPBConfig

