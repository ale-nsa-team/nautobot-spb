from django.urls import path
from nautobot.apps.views import generic
from . import models
from . import views

urlpatterns = [
    path("bvlan/", views.SPB_BVLANListView.as_view(), name="spb_bvlan_list"),
    path("service/", views.SPB_ServiceListView.as_view(), name="spb_service_list"),
    path("sap/", views.SPB_SAPListView.as_view(), name="spb_sap_list"),
    path("sdp/", views.SPB_SDPListView.as_view(), name="spb_sdp_list"),
    path("interface/", views.SPB_InterfaceListView.as_view(), name="spb_interface_list"),
    path("isis/", views.SPB_ISISListView.as_view(), name="spb_isis_list"),
    path("ipvpn_bind/", views.SPB_IPVPNBindListView.as_view(), name="spb_ipvpn_bind_list"),
    path("ipvpn_redist/", views.SPB_IPVPNRedistListView.as_view(), name="spb_ipvpn_redist_list"),
]

