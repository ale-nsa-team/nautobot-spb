from nautobot.apps.tables import BaseTable, ToggleColumn
from nautobot.tables.columns import ActionsColumn
from . import models


#
# === SPB BVLANs ===
#
class SPB_BVLANTable(BaseTable):
    pk = ToggleColumn()
    actions = ActionsColumn(actions=("edit", "delete"))

    class Meta(BaseTable.Meta):
        model = models.SPB_BVLAN
        fields = ("pk", "bvlan_id", "name", "admin_state", "ect_id", "control", "tandem_multicast_mode", "description")
        default_columns = ("bvlan_id", "name", "admin_state", "ect_id")


#
# === SPB Services ===
#
class SPB_ServiceTable(BaseTable):
    pk = ToggleColumn()
    actions = ActionsColumn(actions=("edit", "delete"))

    class Meta(BaseTable.Meta):
        model = models.SPB_Service
        fields = (
            "pk",
            "service_id",
            "isid",
            "bvlan",
            "pseudo_wire",
            "e_tree",
            "multicast_mode",
            "admin_state",
            "description",
        )
        default_columns = ("service_id", "isid", "bvlan", "admin_state")


#
# === SPB SAPs ===
#
class SPB_SAPTable(BaseTable):
    pk = ToggleColumn()
    actions = ActionsColumn(actions=("edit", "delete"))

    class Meta(BaseTable.Meta):
        model = models.SPB_SAP
        fields = ("pk", "service", "device", "interface", "encapsulation", "admin_state")
        default_columns = ("service", "device", "interface", "encapsulation")


#
# === SPB SDPs ===
#
class SPB_SDPTable(BaseTable):
    pk = ToggleColumn()
    actions = ActionsColumn(actions=("edit", "delete"))

    class Meta(BaseTable.Meta):
        model = models.SPB_SDP
        fields = ("pk", "sdp_id", "sysid", "bvlan", "oper_state", "dynamic", "bind_count")
        default_columns = ("sdp_id", "sysid", "bvlan", "oper_state")


#
# === SPB Interfaces ===
#
class SPB_InterfaceTable(BaseTable):
    pk = ToggleColumn()
    actions = ActionsColumn(actions=("edit", "delete"))

    class Meta(BaseTable.Meta):
        model = models.SPB_Interface
        fields = (
            "pk",
            "device",
            "interface",
            "iface_type",
            "hello_interval",
            "hello_multiplier",
            "metric",
            "priority",
            "admin_state",
        )
        default_columns = ("device", "interface", "iface_type", "metric", "priority", "admin_state")


#
# === SPB ISIS ===
#
class SPB_ISISTable(BaseTable):
    pk = ToggleColumn()
    actions = ActionsColumn(actions=("edit", "delete"))

    class Meta(BaseTable.Meta):
        model = models.SPB_ISIS
        fields = (
            "pk",
            "device",
            "bridge_priority",
            "control_bvlan",
            "spf_wait",
            "lsp_wait",
            "graceful_restart",
        )
        default_columns = ("device", "bridge_priority", "control_bvlan")


#
# === SPB IPVPN Bind ===
#
class SPB_IPVPN_BindTable(BaseTable):
    pk = ToggleColumn()
    actions = ActionsColumn(actions=("edit", "delete"))

    class Meta(BaseTable.Meta):
        model = models.SPB_IPVPN_Bind
        fields = ("pk", "vrf", "service", "gateway", "import_route_map", "all_routes")
        default_columns = ("vrf", "service", "gateway", "all_routes")


#
# === SPB IPVPN Redist ===
#
class SPB_IPVPN_RedistTable(BaseTable):
    pk = ToggleColumn()
    actions = ActionsColumn(actions=("edit", "delete"))

    class Meta(BaseTable.Meta):
        model = models.SPB_IPVPN_Redist
        fields = ("pk", "source_vrf", "source_isid", "dest_isid", "route_map", "all_routes")
        default_columns = ("source_vrf", "dest_isid", "all_routes")

