# nautobot_spb/models.py
from django.db import models
from nautobot.extras.models import ChangeLoggedModel
from nautobot.dcim.models import Device, Interface
from nautobot.ipam.models import VLAN
from nautobot.ipam.models import VRF

class SPB_BVLAN(ChangeLoggedModel):
    bvlan_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    admin_state = models.BooleanField(default=True)
    ect_id = models.PositiveSmallIntegerField(blank=True, null=True)  # ECT 1-16
    tandem_multicast_mode = models.CharField(max_length=8, choices=(("sgmode","sgmode"),("gmode","gmode")), default="sgmode")
    control = models.BooleanField(default=False)  # control-bvlan
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"BVLAN {self.bvlan_id} {self.name or ''}"

class SPB_Service(ChangeLoggedModel):
    service_id = models.PositiveIntegerField(unique=True)  # 1-32767 static, >32768 dynamic
    isid = models.PositiveIntegerField()  # 256..16777214
    bvlan = models.ForeignKey(SPB_BVLAN, on_delete=models.PROTECT, related_name="services")
    pseudo_wire = models.BooleanField(default=False)
    e_tree = models.BooleanField(default=False)
    multicast_mode = models.CharField(max_length=10, choices=(("head-end","head-end"),("tandem","tandem"),("hybrid","hybrid")), default="head-end")
    vlan_xlation = models.BooleanField(default=False)
    stats_enabled = models.BooleanField(default=False)
    admin_state = models.BooleanField(default=True)
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ("isid","bvlan")

    def __str__(self):
        return f"SPB service {self.service_id} (ISID {self.isid})"

class SPB_SAP(ChangeLoggedModel):
    service = models.ForeignKey(SPB_Service, on_delete=models.CASCADE, related_name="saps")
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    interface = models.ForeignKey(Interface, on_delete=models.CASCADE)
    encapsulation = models.CharField(max_length=32, default=":all")  # e.g. "1/1/2:all" or ":0"
    admin_state = models.BooleanField(default=True)

    def __str__(self):
        return f"SAP {self.device} {self.interface} -> Service {self.service_id}"

class SPB_SDP(ChangeLoggedModel):
    sdp_id = models.PositiveIntegerField()
    sysid = models.CharField(max_length=32)  # System/BMAC
    bvlan = models.ForeignKey(SPB_BVLAN, on_delete=models.CASCADE)
    source_id = models.CharField(max_length=32, blank=True, null=True)
    oper_state = models.CharField(max_length=16, blank=True)
    dynamic = models.BooleanField(default=True)
    bind_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"SDP {self.sdp_id} ({self.sysid}:{self.bvlan.bvlan_id})"

class SPB_Interface(ChangeLoggedModel):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    interface = models.ForeignKey(Interface, on_delete=models.CASCADE)
    iface_type = models.CharField(max_length=12, choices=(("p2p","p2p"),("multi-access","multi-access")), default="multi-access")
    hello_interval = models.PositiveIntegerField(blank=True, null=True)
    hello_multiplier = models.PositiveIntegerField(blank=True, null=True)
    metric = models.PositiveSmallIntegerField(blank=True, null=True)
    priority = models.PositiveIntegerField(blank=True, null=True)
    admin_state = models.BooleanField(default=True)

    class Meta:
        unique_together = ("device","interface")

    def __str__(self):
        return f"{self.device}:{self.interface} (SPB)"

class SPB_ISIS(ChangeLoggedModel):
    device = models.OneToOneField(Device, on_delete=models.CASCADE)
    bridge_priority = models.PositiveIntegerField(default=32768)
    control_bvlan = models.ForeignKey(SPB_BVLAN, on_delete=models.SET_NULL, blank=True, null=True)
    spf_wait = models.PositiveIntegerField(blank=True, null=True)
    lsp_wait = models.PositiveIntegerField(blank=True, null=True)
    graceful_restart = models.BooleanField(default=False)

    def __str__(self):
        return f"ISIS-SPB on {self.device}"

class SPB_IPVPN_Bind(ChangeLoggedModel):
    vrf = models.ForeignKey(VRF, on_delete=models.CASCADE)
    service = models.ForeignKey(SPB_Service, on_delete=models.CASCADE)  # service.isid maps here
    gateway = models.GenericIPAddressField()
    import_route_map = models.CharField(max_length=128, blank=True)
    all_routes = models.BooleanField(default=False)

    class Meta:
        unique_together = ("vrf","service")

    def __str__(self):
        return f"IPVPN bind VRF {self.vrf} <-> ISID {self.service.isid}"

class SPB_IPVPN_Redist(ChangeLoggedModel):
    source_vrf = models.ForeignKey(VRF, on_delete=models.SET_NULL, blank=True, null=True)
    source_isid = models.ForeignKey(SPB_Service, on_delete=models.SET_NULL, blank=True, null=True, related_name="redist_sources")
    dest_isid = models.ForeignKey(SPB_Service, on_delete=models.CASCADE, related_name="redist_dest")
    route_map = models.CharField(max_length=128, blank=True)
    all_routes = models.BooleanField(default=False)

    def __str__(self):
        return f"Redist {self.source_vrf or self.source_isid} -> ISID {self.dest_isid.isid}"

