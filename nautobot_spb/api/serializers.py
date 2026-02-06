# nautobot_spb/api/serializers.py
from rest_framework import serializers
from nautobot.apps.api import NautobotModelSerializer
from nautobot.dcim.api.serializers import DeviceSerializer, InterfaceSerializer
from nautobot.ipam.api.serializers import VRFSerializer
from nautobot_spb import models


class SPB_BVLANSerializer(NautobotModelSerializer):
    class Meta:
        model = models.SPB_BVLAN
        fields = "__all__"


class SPB_ServiceSerializer(NautobotModelSerializer):
    bvlan = serializers.SerializerMethodField()
    
    class Meta:
        model = models.SPB_Service
        fields = "__all__"
    
    def get_bvlan(self, obj):
        return {"id": str(obj.bvlan.id), "bvlan_id": obj.bvlan.bvlan_id}


class SPB_SAPSerializer(NautobotModelSerializer):
    service = serializers.SerializerMethodField()
    device = serializers.SerializerMethodField()
    interface = serializers.SerializerMethodField()
    
    class Meta:
        model = models.SPB_SAP
        fields = "__all__"
    
    def get_service(self, obj):
        return {"id": str(obj.service.id), "service_id": obj.service.service_id}
    
    def get_device(self, obj):
        return {"id": str(obj.device.id), "name": obj.device.name}
    
    def get_interface(self, obj):
        return {"id": str(obj.interface.id), "name": obj.interface.name}


class SPB_SDPSerializer(NautobotModelSerializer):
    bvlan = serializers.SerializerMethodField()
    
    class Meta:
        model = models.SPB_SDP
        fields = "__all__"
    
    def get_bvlan(self, obj):
        return {"id": str(obj.bvlan.id), "bvlan_id": obj.bvlan.bvlan_id}


class SPB_InterfaceSerializer(NautobotModelSerializer):
    device = serializers.SerializerMethodField()
    interface = serializers.SerializerMethodField()
    
    class Meta:
        model = models.SPB_Interface
        fields = "__all__"
    
    def get_device(self, obj):
        return {"id": str(obj.device.id), "name": obj.device.name}
    
    def get_interface(self, obj):
        return {"id": str(obj.interface.id), "name": obj.interface.name}


class SPB_ISISSerializer(NautobotModelSerializer):
    device = serializers.SerializerMethodField()
    bvlan = serializers.SerializerMethodField()

    class Meta:
        model = models.SPB_ISIS
        fields = "__all__"

    def get_device(self, obj):
        return {"id": str(obj.device.id), "name": obj.device.name}

    def get_bvlan(self, obj):
        if obj.bvlan:
            return {"id": str(obj.bvlan.id), "bvlan_id": obj.bvlan.bvlan_id}
        return None


class SPB_IPVPN_BindSerializer(NautobotModelSerializer):
    vrf = serializers.SerializerMethodField()
    service = serializers.SerializerMethodField()
    
    class Meta:
        model = models.SPB_IPVPN_Bind
        fields = "__all__"
    
    def get_vrf(self, obj):
        return {"id": str(obj.vrf.id), "name": obj.vrf.name}
    
    def get_service(self, obj):
        return {"id": str(obj.service.id), "service_id": obj.service.service_id}


class SPB_IPVPN_RedistSerializer(NautobotModelSerializer):
    source_vrf = serializers.SerializerMethodField()
    source_isid = serializers.SerializerMethodField()
    dest_isid = serializers.SerializerMethodField()
    
    class Meta:
        model = models.SPB_IPVPN_Redist
        fields = "__all__"
    
    def get_source_vrf(self, obj):
        if obj.source_vrf:
            return {"id": str(obj.source_vrf.id), "name": obj.source_vrf.name}
        return None
    
    def get_source_isid(self, obj):
        if obj.source_isid:
            return {"id": str(obj.source_isid.id), "isid": obj.source_isid.isid}
        return None
    
    def get_dest_isid(self, obj):
        return {"id": str(obj.dest_isid.id), "isid": obj.dest_isid.isid}
