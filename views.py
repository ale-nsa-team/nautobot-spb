# nautobot_spb/views.py
from nautobot.apps.views import (
    ObjectListView,
    ObjectView,
    ObjectEditView,
    ObjectDeleteView,
    BulkDeleteView,
    BulkImportView,
)
from . import models, tables, forms
from nautobot.core.views.generic import ObjectEditView
from django.shortcuts import render, redirect
from .forms import SPBSAPForm


# === BVLAN Views ===
class SPBBVLANListView(ObjectListView):
    queryset = models.SPB_BVLAN.objects.all()
    table = tables.SPB_BVLANTable
    filterset_class = forms.SPBBVLANFilterForm


class SPBBVLANView(ObjectView):
    queryset = models.SPB_BVLAN.objects.all()
    template_name = "nautobot_spb/spb_bvlan.html"


class SPBBVLANEditView(ObjectEditView):
    queryset = models.SPB_BVLAN.objects.all()
    model_form = forms.SPBBVLANForm
    default_return_url = "plugins:nautobot_spb:spb_bvlan_list"


class SPBBVLANDeleteView(ObjectDeleteView):
    queryset = models.SPB_BVLAN.objects.all()
    default_return_url = "plugins:nautobot_spb:spb_bvlan_list"


class SPBBVLANBulkDeleteView(BulkDeleteView):
    queryset = models.SPB_BVLAN.objects.all()
    table = tables.SPB_BVLANTable
    filterset_class = forms.SPBBVLANFilterForm
    default_return_url = "plugins:nautobot_spb:spb_bvlan_list"


class SPBBVLANBulkImportView(BulkImportView):
    queryset = models.SPB_BVLAN.objects.all()
    table = tables.SPB_BVLANTable


# === Service Views ===
class SPBServiceListView(ObjectListView):
    queryset = models.SPB_Service.objects.all()
    table = tables.SPB_ServiceTable
    filterset_class = forms.SPBServiceFilterForm


class SPBServiceView(ObjectView):
    queryset = models.SPB_Service.objects.all()
    template_name = "nautobot_spb/spb_service.html"


class SPBServiceEditView(ObjectEditView):
    queryset = models.SPB_Service.objects.all()
    model_form = forms.SPBServiceForm
    default_return_url = "plugins:nautobot_spb:spb_service_list"


class SPBServiceDeleteView(ObjectDeleteView):
    queryset = models.SPB_Service.objects.all()
    default_return_url = "plugins:nautobot_spb:spb_service_list"


class SPBServiceBulkDeleteView(BulkDeleteView):
    queryset = models.SPB_Service.objects.all()
    table = tables.SPB_ServiceTable
    default_return_url = "plugins:nautobot_spb:spb_service_list"


class SPBServiceBulkImportView(BulkImportView):
    queryset = models.SPB_Service.objects.all()
    model_form = forms.SPBServiceCSVForm
    table = tables.SPB_ServiceTable


# === SAP Views ===
class SPBSAPListView(ObjectListView):
    queryset = models.SPB_SAP.objects.all()
    table = tables.SPB_SAPTable


class SPBSAPView(ObjectView):
    queryset = models.SPB_SAP.objects.all()
    template_name = "nautobot_spb/spb_sap.html"


#class SPBSAPEditView(ObjectEditView):
#    queryset = models.SPB_SAP.objects.all()
#    model_form = forms.SPBSAPForm
#    default_return_url = "plugins:nautobot_spb:spb_sap_list"
class SPBSAPEditView(ObjectEditView):
    queryset = models.SPB_SAP.objects.all()
    model_form = forms.SPBSAPForm
    default_return_url = "plugins:nautobot_spb:spb_sap_list"
#    template_name = "nautobot_spb/spb_sap_edit.html"


class SPBSAPDeleteView(ObjectDeleteView):
    queryset = models.SPB_SAP.objects.all()
    default_return_url = "plugins:nautobot_spb:spb_sap_list"
    template_name = "generic/object_delete.html"

class SPBSAPBulkDeleteView(BulkDeleteView):
    queryset = models.SPB_SAP.objects.all()
    table = tables.SPB_SAPTable
    default_return_url = "plugins:nautobot_spb:spb_sap_list"


class SPBSAPBulkImportView(BulkImportView):
    queryset = models.SPB_SAP.objects.all()
    table = tables.SPB_SAPTable


# === SDP Views ===
class SPBSDPListView(ObjectListView):
    queryset = models.SPB_SDP.objects.all()
    table = tables.SPB_SDPTable


class SPBSDPView(ObjectView):
    queryset = models.SPB_SDP.objects.all()
    template_name = "nautobot_spb/spb_sdp.html"


class SPBSDPEditView(ObjectEditView):
    queryset = models.SPB_SDP.objects.all()
    model_form = forms.SPBSDPForm
    default_return_url = "plugins:nautobot_spb:spb_sdp_list"


class SPBSDPDeleteView(ObjectDeleteView):
    queryset = models.SPB_SDP.objects.all()
    default_return_url = "plugins:nautobot_spb:spb_sdp_list"


class SPBSDPBulkDeleteView(BulkDeleteView):
    queryset = models.SPB_SDP.objects.all()
    table = tables.SPB_SDPTable
    default_return_url = "plugins:nautobot_spb:spb_sdp_list"


class SPBSDPBulkImportView(BulkImportView):
    queryset = models.SPB_SDP.objects.all()
    table = tables.SPB_SDPTable


# === Interface Views ===
class SPBInterfaceListView(ObjectListView):
    queryset = models.SPB_Interface.objects.all()
    table = tables.SPB_InterfaceTable


class SPBInterfaceView(ObjectView):
    queryset = models.SPB_Interface.objects.all()
    template_name = "nautobot_spb/spb_interface.html"


class SPBInterfaceEditView(ObjectEditView):
    queryset = models.SPB_Interface.objects.all()
    model_form = forms.SPBInterfaceForm
    default_return_url = "plugins:nautobot_spb:spb_interface_list"


class SPBInterfaceDeleteView(ObjectDeleteView):
    queryset = models.SPB_Interface.objects.all()
    default_return_url = "plugins:nautobot_spb:spb_interface_list"


class SPBInterfaceBulkDeleteView(BulkDeleteView):
    queryset = models.SPB_Interface.objects.all()
    table = tables.SPB_InterfaceTable
    default_return_url = "plugins:nautobot_spb:spb_interface_list"


class SPBInterfaceBulkImportView(BulkImportView):
    queryset = models.SPB_Interface.objects.all()
    table = tables.SPB_InterfaceTable


# === ISIS Views ===
class SPBISISListView(ObjectListView):
    queryset = models.SPB_ISIS.objects.all()
    table = tables.SPB_ISISTable


class SPBISISView(ObjectView):
    queryset = models.SPB_ISIS.objects.all()
    template_name = "nautobot_spb/spb_isis.html"


class SPBISISEditView(ObjectEditView):
    queryset = models.SPB_ISIS.objects.all()
    model_form = forms.SPBISISForm
    default_return_url = "plugins:nautobot_spb:spb_isis_list"


class SPBISISDeleteView(ObjectDeleteView):
    queryset = models.SPB_ISIS.objects.all()
    default_return_url = "plugins:nautobot_spb:spb_isis_list"


class SPBISISBulkDeleteView(BulkDeleteView):
    queryset = models.SPB_ISIS.objects.all()
    table = tables.SPB_ISISTable
    default_return_url = "plugins:nautobot_spb:spb_isis_list"


class SPBISISBulkImportView(BulkImportView):
    queryset = models.SPB_ISIS.objects.all()
    table = tables.SPB_ISISTable


# === IPVPN Bind Views ===
class SPBIPVPNBindListView(ObjectListView):
    queryset = models.SPB_IPVPN_Bind.objects.all()
    table = tables.SPB_IPVPN_BindTable


class SPBIPVPNBindView(ObjectView):
    queryset = models.SPB_IPVPN_Bind.objects.all()
    template_name = "nautobot_spb/spb_ipvpn_bind.html"


class SPBIPVPNBindEditView(ObjectEditView):
    queryset = models.SPB_IPVPN_Bind.objects.all()
    model_form = forms.SPBIPVPNBindForm
    default_return_url = "plugins:nautobot_spb:spb_ipvpn_bind_list"


class SPBIPVPNBindDeleteView(ObjectDeleteView):
    queryset = models.SPB_IPVPN_Bind.objects.all()
    default_return_url = "plugins:nautobot_spb:spb_ipvpn_bind_list"


class SPBIPVPNBindBulkDeleteView(BulkDeleteView):
    queryset = models.SPB_IPVPN_Bind.objects.all()
    table = tables.SPB_IPVPN_BindTable
    default_return_url = "plugins:nautobot_spb:spb_ipvpn_bind_list"


class SPBIPVPNBindBulkImportView(BulkImportView):
    queryset = models.SPB_IPVPN_Bind.objects.all()
    table = tables.SPB_IPVPN_BindTable


# === IPVPN Redist Views ===
class SPBIPVPNRedistListView(ObjectListView):
    queryset = models.SPB_IPVPN_Redist.objects.all()
    table = tables.SPB_IPVPN_RedistTable


class SPBIPVPNRedistView(ObjectView):
    queryset = models.SPB_IPVPN_Redist.objects.all()
    template_name = "nautobot_spb/spb_ipvpn_redist.html"


class SPBIPVPNRedistEditView(ObjectEditView):
    queryset = models.SPB_IPVPN_Redist.objects.all()
    model_form = forms.SPBIPVPNRedistForm
    default_return_url = "plugins:nautobot_spb:spb_ipvpn_redist_list"


class SPBIPVPNRedistDeleteView(ObjectDeleteView):
    queryset = models.SPB_IPVPN_Redist.objects.all()
    default_return_url = "plugins:nautobot_spb:spb_ipvpn_redist_list"


class SPBIPVPNRedistBulkDeleteView(BulkDeleteView):
    queryset = models.SPB_IPVPN_Redist.objects.all()
    table = tables.SPB_IPVPN_RedistTable
    default_return_url = "plugins:nautobot_spb:spb_ipvpn_redist_list"


class SPBIPVPNRedistBulkImportView(BulkImportView):
    queryset = models.SPB_IPVPN_Redist.objects.all()
    table = tables.SPB_IPVPN_RedistTable





# === Topology Views ===
# === TOPOLOGY VIEWS ===

class SPBTopologyListView(ObjectListView):
    queryset = models.SPB_Topology.objects.all()
    table = tables.SPBTopologyTable
    action_buttons = ("add",)


class SPBTopologyView(ObjectView):
    queryset = models.SPB_Topology.objects.all()
    template_name = "nautobot_spb/spb_topology.html"
    #template_name = "generic/object_view.html"
    action_buttons = ("edit", "delete")

class SPBTopologyEditView(ObjectEditView):
    queryset = models.SPB_Topology.objects.all()
    model_form = forms.SPBTopologyForm
    default_return_url = "plugins:nautobot_spb:spb_topology_list"
    template_name = "nautobot_spb/spb_topology_edit.html"

class SPBTopologyDeleteView(ObjectDeleteView):
    """Delete view for a single SPB Topology."""
    queryset = models.SPB_Topology.objects.all()
    default_return_url = "plugins:nautobot_spb:spb_topology_list"
