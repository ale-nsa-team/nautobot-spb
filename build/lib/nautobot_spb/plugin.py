from nautobot.apps import NautobotAppConfig

class NautobotSPBConfig(NautobotAppConfig):
    name = "nautobot_spb"
    verbose_name = "Nautobot SPB"
    version = "0.1"
    min_version = "2.4.0"
    description = "Plugin SPB pour Nautobot"
    author = "Lina"
    author_email = "your.email@example.com"
    base_url = "spb"

    def ready(self):
        """Register admin objects and skip URL auto-load."""
        from . import admin  # noqa: F401
        self.urls = []

