# nautobot_spb/api/views.py
from nautobot.apps.api import NautobotModelViewSet
from nautobot_spb import models
from nautobot_spb.api import serializers


class SPBBVLANViewSet(NautobotModelViewSet):
    queryset = models.SPB_BVLAN.objects.all()
    serializer_class = serializers.SPB_BVLANSerializer


class SPBServiceViewSet(NautobotModelViewSet):
    queryset = models.SPB_Service.objects.all()
    serializer_class = serializers.SPB_ServiceSerializer


class SPBSAPViewSet(NautobotModelViewSet):
    queryset = models.SPB_SAP.objects.all()
    serializer_class = serializers.SPB_SAPSerializer


class SPBSDPViewSet(NautobotModelViewSet):
    queryset = models.SPB_SDP.objects.all()
    serializer_class = serializers.SPB_SDPSerializer


class SPBInterfaceViewSet(NautobotModelViewSet):
    queryset = models.SPB_Interface.objects.all()
    serializer_class = serializers.SPB_InterfaceSerializer


class SPBISISViewSet(NautobotModelViewSet):
    queryset = models.SPB_ISIS.objects.all()
    serializer_class = serializers.SPB_ISISSerializer


class SPBIPVPNBindViewSet(NautobotModelViewSet):
    queryset = models.SPB_IPVPN_Bind.objects.all()
    serializer_class = serializers.SPB_IPVPN_BindSerializer


class SPBIPVPNRedistViewSet(NautobotModelViewSet):
    queryset = models.SPB_IPVPN_Redist.objects.all()
    serializer_class = serializers.SPB_IPVPN_RedistSerializer
