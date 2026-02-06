# nautobot_spb/registration.py

from nautobot.extras import registry
from nautobot_spb import models


def register_spb_models_for_features():
    """Register SPB models for Webhooks and Change Logging."""
    try:
        # Get the model_features registry safely
        model_features = getattr(registry, "model_features", None)
        if model_features is None:
            print("⚠️ model_features registry not found in Nautobot extras.registry")
            return

        spb_models = [
            models.SPB_BVLAN,
            models.SPB_Service,
            models.SPB_Interface,
            models.SPB_ISIS,
            models.SPB_SAP,
            models.SPB_SDP,
            models.SPB_IPVPN_Bind,
            models.SPB_IPVPN_Redist,
        ]

        # Register each SPB model for webhooks and change logging
        for model in spb_models:
            model_features["webhooks"].add(model)
            model_features["change_logging"].add(model)

        print("✅ SPB models registered for webhooks and change logging.")

    except Exception as e:
        print(f"⚠️ Could not auto-register SPB models: {e}")

