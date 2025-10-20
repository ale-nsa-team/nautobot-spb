from nautobot.extras.plugins import FeatureQuery

# Liste des modèles SPB à exposer à Nautobot Extras
models = [
    "SPB_BVLAN",
    "SPB_Service",
    "SPB_SAP",
    "SPB_SDP",
    "SPB_Interface",
    "SPB_ISIS",
    "SPB_IPVPN_Bind",
    "SPB_IPVPN_Redist",
]

# Enregistre tous ces modèles comme "webhook-enabled"
FeatureQuery.register(
    feature="webhooks",
    app_label="nautobot_spb",
    models=models,
)

