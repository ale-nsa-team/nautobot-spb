from django.contrib import admin
from .models import (
    SPB_BVLAN,
    SPB_Service,
    SPB_SAP,
    SPB_SDP,
    SPB_Interface,
    SPB_ISIS,
    SPB_IPVPN_Bind,
    SPB_IPVPN_Redist,
)

# Register each model so they appear in Admin
@admin.register(SPB_BVLAN)
class SPBBVLANAdmin(admin.ModelAdmin):
    list_display = ("bvlan_id", "name", "admin_state")
    search_fields = ("bvlan_id", "name")


@admin.register(SPB_Service)
class SPBServiceAdmin(admin.ModelAdmin):
    list_display = ("service_id", "isid", "bvlan", "admin_state")
    search_fields = ("service_id", "isid", "description")


@admin.register(SPB_SAP)
class SPBSAPAdmin(admin.ModelAdmin):
    list_display = ("service", "device", "interface", "encapsulation", "admin_state")


@admin.register(SPB_SDP)
class SPBSDPAdmin(admin.ModelAdmin):
    list_display = ("sdp_id", "sysid", "bvlan", "oper_state", "dynamic")


@admin.register(SPB_Interface)
class SPBInterfaceAdmin(admin.ModelAdmin):
    list_display = ("device", "interface", "iface_type", "metric", "priority")


@admin.register(SPB_ISIS)
class SPBISISAdmin(admin.ModelAdmin):
    list_display = ("device", "bridge_priority", "control_bvlan")


@admin.register(SPB_IPVPN_Bind)
class SPBIPVPNBindAdmin(admin.ModelAdmin):
    list_display = ("vrf", "service", "gateway", "all_routes")


@admin.register(SPB_IPVPN_Redist)
class SPBIPVPNRedistAdmin(admin.ModelAdmin):
    list_display = ("source_vrf", "source_isid", "dest_isid", "all_routes")

