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
    #urlpatterns = "nautobot_spb.urls"

    def ready(self):
        """Called when Nautobot starts and plugin is loaded."""
        from . import admin  # noqa

