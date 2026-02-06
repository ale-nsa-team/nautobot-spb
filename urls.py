from django.urls import path
from . import views

app_name = "nautobot_spb"

urlpatterns = [
    # BVLAN URLs
    path("bvlan/", views.SPBBVLANListView.as_view(), name="spb_bvlan_list"),
    path("bvlan/add/", views.SPBBVLANEditView.as_view(), name="spb_bvlan_add"),
    path("bvlan/import/", views.SPBBVLANBulkImportView.as_view(), name="spb_bvlan_import"),
    path("bvlan/<uuid:pk>/", views.SPBBVLANView.as_view(), name="spb_bvlan"),
    path("bvlan/<uuid:pk>/edit/", views.SPBBVLANEditView.as_view(), name="spb_bvlan_edit"),
    path("bvlan/<uuid:pk>/delete/", views.SPBBVLANDeleteView.as_view(), name="spb_bvlan_delete"),
    path("bvlan/delete/", views.SPBBVLANBulkDeleteView.as_view(), name="spb_bvlan_bulk_delete"),

    # Service URLs
    path("service/", views.SPBServiceListView.as_view(), name="spb_service_list"),
    path("service/add/", views.SPBServiceEditView.as_view(), name="spb_service_add"),
    path("service/import/", views.SPBServiceBulkImportView.as_view(), name="spb_service_import"),
    path("service/<uuid:pk>/", views.SPBServiceView.as_view(), name="spb_service"),
    path("service/<uuid:pk>/edit/", views.SPBServiceEditView.as_view(), name="spb_service_edit"),
    path("service/<uuid:pk>/delete/", views.SPBServiceDeleteView.as_view(), name="spb_service_delete"),
    path("service/delete/", views.SPBServiceBulkDeleteView.as_view(), name="spb_service_bulk_delete"),

    # SAP URLs
    path("sap/", views.SPBSAPListView.as_view(), name="spb_sap_list"),
    path("sap/add/", views.SPBSAPEditView.as_view(), name="spb_sap_add"),
    path("sap/import/", views.SPBSAPBulkImportView.as_view(), name="spb_sap_import"),
    path("sap/<uuid:pk>/", views.SPBSAPView.as_view(), name="spb_sap"),
    path("sap/<uuid:pk>/edit/", views.SPBSAPEditView.as_view(), name="spb_sap_edit"),
    path("sap/<uuid:pk>/delete/", views.SPBSAPDeleteView.as_view(), name="spb_sap_delete"),
    path("sap/delete/", views.SPBSAPBulkDeleteView.as_view(), name="spb_sap_bulk_delete"),

    # SDP URLs
    path("sdp/", views.SPBSDPListView.as_view(), name="spb_sdp_list"),
    path("sdp/add/", views.SPBSDPEditView.as_view(), name="spb_sdp_add"),
    path("sdp/import/", views.SPBSDPBulkImportView.as_view(), name="spb_sdp_import"),
    path("sdp/<uuid:pk>/", views.SPBSDPView.as_view(), name="spb_sdp"),
    path("sdp/<uuid:pk>/edit/", views.SPBSDPEditView.as_view(), name="spb_sdp_edit"),
    path("sdp/<uuid:pk>/delete/", views.SPBSDPDeleteView.as_view(), name="spb_sdp_delete"),
    path("sdp/delete/", views.SPBSDPBulkDeleteView.as_view(), name="spb_sdp_bulk_delete"),

    # Interface URLs
    path("interface/", views.SPBInterfaceListView.as_view(), name="spb_interface_list"),
    path("interface/add/", views.SPBInterfaceEditView.as_view(), name="spb_interface_add"),
    path("interface/import/", views.SPBInterfaceBulkImportView.as_view(), name="spb_interface_import"),
    path("interface/<uuid:pk>/", views.SPBInterfaceView.as_view(), name="spb_interface"),
    path("interface/<uuid:pk>/edit/", views.SPBInterfaceEditView.as_view(), name="spb_interface_edit"),
    path("interface/<uuid:pk>/delete/", views.SPBInterfaceDeleteView.as_view(), name="spb_interface_delete"),
    path("interface/delete/", views.SPBInterfaceBulkDeleteView.as_view(), name="spb_interface_bulk_delete"),

    # ISIS URLs
    path("isis/", views.SPBISISListView.as_view(), name="spb_isis_list"),
    path("isis/add/", views.SPBISISEditView.as_view(), name="spb_isis_add"),
    path("isis/import/", views.SPBISISBulkImportView.as_view(), name="spb_isis_import"),
    path("isis/<uuid:pk>/", views.SPBISISView.as_view(), name="spb_isis"),
    path("isis/<uuid:pk>/edit/", views.SPBISISEditView.as_view(), name="spb_isis_edit"),
    path("isis/<uuid:pk>/delete/", views.SPBISISDeleteView.as_view(), name="spb_isis_delete"),
    path("isis/delete/", views.SPBISISBulkDeleteView.as_view(), name="spb_isis_bulk_delete"),

    # IPVPN Bind URLs
    path("ipvpn-bind/", views.SPBIPVPNBindListView.as_view(), name="spb_ipvpn_bind_list"),
    path("ipvpn-bind/add/", views.SPBIPVPNBindEditView.as_view(), name="spb_ipvpn_bind_add"),
    path("ipvpn-bind/import/", views.SPBIPVPNBindBulkImportView.as_view(), name="spb_ipvpn_bind_import"),
    path("ipvpn-bind/<uuid:pk>/", views.SPBIPVPNBindView.as_view(), name="spb_ipvpn_bind"),
    path("ipvpn-bind/<uuid:pk>/edit/", views.SPBIPVPNBindEditView.as_view(), name="spb_ipvpn_bind_edit"),
    path("ipvpn-bind/<uuid:pk>/delete/", views.SPBIPVPNBindDeleteView.as_view(), name="spb_ipvpn_bind_delete"),
    path("ipvpn-bind/delete/", views.SPBIPVPNBindBulkDeleteView.as_view(), name="spb_ipvpn_bind_bulk_delete"),

    # IPVPN Redist URLs
    path("ipvpn-redist/", views.SPBIPVPNRedistListView.as_view(), name="spb_ipvpn_redist_list"),
    path("ipvpn-redist/add/", views.SPBIPVPNRedistEditView.as_view(), name="spb_ipvpn_redist_add"),
    path("ipvpn-redist/import/", views.SPBIPVPNRedistBulkImportView.as_view(), name="spb_ipvpn_redist_import"),
    path("ipvpn-redist/<uuid:pk>/", views.SPBIPVPNRedistView.as_view(), name="spb_ipvpn_redist"),
    path("ipvpn-redist/<uuid:pk>/edit/", views.SPBIPVPNRedistEditView.as_view(), name="spb_ipvpn_redist_edit"),
    path("ipvpn-redist/<uuid:pk>/delete/", views.SPBIPVPNRedistDeleteView.as_view(), name="spb_ipvpn_redist_delete"),
    path("ipvpn-redist/delete/", views.SPBIPVPNRedistBulkDeleteView.as_view(), name="spb_ipvpn_redist_bulk_delete"),

    # Topology URLs
    path("topology/", views.SPBTopologyListView.as_view(), name="spb_topology_list"),
    path("topology/add/", views.SPBTopologyEditView.as_view(), name="spb_topology_add"),
    path("topology/<uuid:pk>/", views.SPBTopologyView.as_view(), name="spb_topology"),
    path("topology/<uuid:pk>/edit/", views.SPBTopologyEditView.as_view(), name="spb_topology_edit"),
    path("topology/<uuid:pk>/delete/", views.SPBTopologyDeleteView.as_view(), name="spb_topology_delete"),

]








