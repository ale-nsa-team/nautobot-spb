from django.urls import path
from . import views

app_name = "nautobot_spb"

urlpatterns = [
    # BVLAN URLs
    path("bvlan/", views.SPBBVLANListView.as_view(), name="spb_bvlan_list"),
    path("bvlan/add/", views.SPBBVLANEditView.as_view(), name="spb_bvlan_add"),
    path("bvlan/<uuid:pk>/", views.SPBBVLANView.as_view(), name="spb_bvlan"),
    path("bvlan/<uuid:pk>/edit/", views.SPBBVLANEditView.as_view(), name="spb_bvlan_edit"),
    path("bvlan/<uuid:pk>/delete/", views.SPBBVLANDeleteView.as_view(), name="spb_bvlan_delete"),
    path("bvlan/delete/", views.SPBBVLANBulkDeleteView.as_view(), name="spb_bvlan_bulk_delete"),
    
    # Service URLs
    path("service/", views.SPBServiceListView.as_view(), name="spb_service_list"),
    path("service/add/", views.SPBServiceEditView.as_view(), name="spb_service_add"),
    path("service/<uuid:pk>/", views.SPBServiceView.as_view(), name="spb_service"),
    path("service/<uuid:pk>/edit/", views.SPBServiceEditView.as_view(), name="spb_service_edit"),
    path("service/<uuid:pk>/delete/", views.SPBServiceDeleteView.as_view(), name="spb_service_delete"),
    
    # Continue for all other models...
    path("interface/", views.SPBInterfaceListView.as_view(), name="spb_interface_list"),
    path("isis/", views.SPBISISListView.as_view(), name="spb_isis_list"),
    path("ipvpn_bind/", views.SPBIPVPNBindListView.as_view(), name="spb_ipvpn_bind_list"),
    path("ipvpn_redist/", views.SPBIPVPNRedistListView.as_view(), name="spb_ipvpn_redist_list"),
]
