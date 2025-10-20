from nautobot.apps.views import generic
from . import models, tables

class SPB_BVLANListView(generic.ObjectListView):
    queryset = models.SPB_BVLAN.objects.all()
    table = tables.SPB_BVLANTable

class SPB_ServiceListView(generic.ObjectListView):
    queryset = models.SPB_Service.objects.all()
    table = tables.SPB_ServiceTable

class SPB_SAPListView(generic.ObjectListView):
    queryset = models.SPB_SAP.objects.all()
    table = tables.SPB_SAPTable

class SPB_SDPListView(generic.ObjectListView):
    queryset = models.SPB_SDP.objects.all()
    table = tables.SPB_SDPTable

class SPB_InterfaceListView(generic.ObjectListView):
    queryset = models.SPB_Interface.objects.all()
    table = tables.SPB_InterfaceTable

class SPB_ISISListView(generic.ObjectListView):
    queryset = models.SPB_ISIS.objects.all()
    table = tables.SPB_ISISTable

class SPB_IPVPNBindListView(generic.ObjectListView):
    queryset = models.SPB_IPVPN_Bind.objects.all()
    table = tables.SPB_IPVPN_BindTable

class SPB_IPVPNRedistListView(generic.ObjectListView):
    queryset = models.SPB_IPVPN_Redist.objects.all()
    table = tables.SPB_IPVPN_RedistTable

