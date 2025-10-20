from nautobot.apps import NautobotAppConfig


class NautobotSPBConfig(NautobotAppConfig):
    """
    Nautobot SPB Plugin Configuration
    """

    # Basic app metadata
    name = "nautobot_spb"
    label = "nautobot_spb"
    verbose_name = "Nautobot SPB"
    version = "0.1"
    min_version = "2.4.0"
    description = "Plugin SPB pour Nautobot (Shortest Path Bridging)"
    author = "Lina"
    author_email = "your.email@example.com"
    base_url = "spb"

    # Optional plugin configuration
    required_settings = []
    default_settings = {}
    caching_config = {}

    # Optional extension modules (UI tabs, nav menu, etc.)
    app_extensions = [
        "nautobot_spb.extend",      # Add custom tabs for Devices/Interfaces
    ]
    navigation = "nautobot_spb.navigation"
    def ready(self):
        """
        Called when Nautobot starts and plugin is loaded.
        Use it to import admin, signals, etc.
        """
        from . import admin  # noqa: F401
        from . import features 
        # disable auto URL registration since we define our own
        self.urls = []
# --- Ensure ContentTypes exist for SPB models ---
        from django.apps import apps
        from django.contrib.contenttypes.models import ContentType
        app_config = apps.get_app_config("nautobot_spb")
        for model in app_config.get_models():
            ContentType.objects.get_or_create(
                app_label="nautobot_spb",
                model=model._meta.model_name
            )
