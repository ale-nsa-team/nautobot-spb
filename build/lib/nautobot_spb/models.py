# nautobot_spb/models.py
from django.db import models
from django.urls import reverse
from nautobot.apps.models import PrimaryModel  # ← Changed from ChangeLoggedModel
from nautobot.dcim.models import Device, Interface
from nautobot.ipam.models import VRF


class SPB_BVLAN(PrimaryModel):  # ← Changed from ChangeLoggedModel
    bvlan_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    admin_state = models.BooleanField(default=True)
    ect_id = models.PositiveSmallIntegerField(blank=True, null=True)  # ECT 1-16
    tandem_multicast_mode = models.CharField(
        max_length=8, 
        choices=(("sgmode", "sgmode"), ("gmode", "gmode")), 
        default="sgmode"
    )
    control = models.BooleanField(default=False)  # control-bvlan
    description = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["bvlan_id"]
        verbose_name = "SPB BVLAN"
        verbose_name_plural = "SPB BVLANs"

    def __str__(self):
        return f"BVLAN {self.bvlan_id} {self.name or ''}"
    
    def get_absolute_url(self):
        return reverse("plugins:nautobot_spb:spb_bvlan", kwargs={"pk": self.pk})


class SPB_Service(PrimaryModel):  # ← Changed
    service_id = models.PositiveIntegerField(unique=True)  # 1-32767 static, >32768 dynamic
    isid = models.PositiveIntegerField()  # 256..16777214
    bvlan = models.ForeignKey(SPB_BVLAN, on_delete=models.PROTECT, related_name="services")
    pseudo_wire = models.BooleanField(default=False)
    e_tree = models.BooleanField(default=False)
    multicast_mode = models.CharField(
        max_length=10,
        choices=(("head-end", "head-end"), ("tandem", "tandem"), ("hybrid", "hybrid")),
        default="head-end"
    )
    vlan_xlation = models.BooleanField(default=False)
    stats_enabled = models.BooleanField(default=False)
    admin_state = models.BooleanField(default=True)
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["service_id"]
        unique_together = ("isid", "bvlan")
        verbose_name = "SPB Service"
        verbose_name_plural = "SPB Services"

    def __str__(self):
        return f"SPB service {self.service_id} (ISID {self.isid})"
    
    def get_absolute_url(self):
        return reverse("plugins:nautobot_spb:spb_service", kwargs={"pk": self.pk})


class SPB_SAP(PrimaryModel):  # ← Changed
    service = models.ForeignKey(SPB_Service, on_delete=models.CASCADE, related_name="saps")
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    interface = models.ForeignKey(Interface, on_delete=models.CASCADE)
    encapsulation = models.CharField(max_length=32, default=":all")  # e.g. "1/1/2:all" or ":0"
    admin_state = models.BooleanField(default=True)

    class Meta:
        ordering = ["device", "interface"]
        verbose_name = "SPB SAP"
        verbose_name_plural = "SPB SAPs"

    def __str__(self):
        return f"SAP {self.device} {self.interface} -> Service {self.service.service_id}"
    
    def get_absolute_url(self):
        return reverse("plugins:nautobot_spb:spb_sap", kwargs={"pk": self.pk})


class SPB_SDP(PrimaryModel):  # ← Changed
    sdp_id = models.PositiveIntegerField()
    sysid = models.CharField(max_length=32)  # System/BMAC
    bvlan = models.ForeignKey(SPB_BVLAN, on_delete=models.CASCADE)
    source_id = models.CharField(max_length=32, blank=True, null=True)
    oper_state = models.CharField(max_length=16, blank=True)
    dynamic = models.BooleanField(default=True)
    bind_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sdp_id"]
        verbose_name = "SPB SDP"
        verbose_name_plural = "SPB SDPs"

    def __str__(self):
        return f"SDP {self.sdp_id} ({self.sysid}:{self.bvlan.bvlan_id})"
    
    def get_absolute_url(self):
        return reverse("plugins:nautobot_spb:spb_sdp", kwargs={"pk": self.pk})


class SPB_Interface(PrimaryModel):  # ← Changed
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    interface = models.ForeignKey(Interface, on_delete=models.CASCADE)
    iface_type = models.CharField(
        max_length=12,
        choices=(("p2p", "p2p"), ("multi-access", "multi-access")),
        default="multi-access"
    )
    hello_interval = models.PositiveIntegerField(blank=True, null=True)
    hello_multiplier = models.PositiveIntegerField(blank=True, null=True)
    metric = models.PositiveSmallIntegerField(blank=True, null=True)
    priority = models.PositiveIntegerField(blank=True, null=True)
    admin_state = models.BooleanField(default=True)

    class Meta:
        ordering = ["device", "interface"]
        unique_together = ("device", "interface")
        verbose_name = "SPB Interface"
        verbose_name_plural = "SPB Interfaces"

    def __str__(self):
        return f"{self.device}:{self.interface} (SPB)"
    
    def get_absolute_url(self):
        return reverse("plugins:nautobot_spb:spb_interface", kwargs={"pk": self.pk})


class SPB_ISIS(PrimaryModel):  # ← Changed
    device = models.OneToOneField(Device, on_delete=models.CASCADE)
    bridge_priority = models.PositiveIntegerField(default=32768)
    control_bvlan = models.ForeignKey(SPB_BVLAN, on_delete=models.SET_NULL, blank=True, null=True)
    spf_wait = models.PositiveIntegerField(blank=True, null=True)
    lsp_wait = models.PositiveIntegerField(blank=True, null=True)
    graceful_restart = models.BooleanField(default=False)

    class Meta:
        ordering = ["device"]
        verbose_name = "SPB ISIS Instance"
        verbose_name_plural = "SPB ISIS Instances"

    def __str__(self):
        return f"ISIS-SPB on {self.device}"
    
    def get_absolute_url(self):
        return reverse("plugins:nautobot_spb:spb_isis", kwargs={"pk": self.pk})


class SPB_IPVPN_Bind(PrimaryModel):  # ← Changed
    vrf = models.ForeignKey(VRF, on_delete=models.CASCADE)
    service = models.ForeignKey(SPB_Service, on_delete=models.CASCADE)  # service.isid maps here
    gateway = models.GenericIPAddressField()
    import_route_map = models.CharField(max_length=128, blank=True)
    all_routes = models.BooleanField(default=False)

    class Meta:
        ordering = ["vrf", "service"]
        unique_together = ("vrf", "service")
        verbose_name = "SPB IPVPN Binding"
        verbose_name_plural = "SPB IPVPN Bindings"

    def __str__(self):
        return f"IPVPN bind VRF {self.vrf} <-> ISID {self.service.isid}"
    
    def get_absolute_url(self):
        return reverse("plugins:nautobot_spb:spb_ipvpn_bind", kwargs={"pk": self.pk})


class SPB_IPVPN_Redist(PrimaryModel):  # ← Changed
    source_vrf = models.ForeignKey(VRF, on_delete=models.SET_NULL, blank=True, null=True)
    source_isid = models.ForeignKey(
        SPB_Service, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True, 
        related_name="redist_sources"
    )
    dest_isid = models.ForeignKey(SPB_Service, on_delete=models.CASCADE, related_name="redist_dest")
    route_map = models.CharField(max_length=128, blank=True)
    all_routes = models.BooleanField(default=False)

    class Meta:
        ordering = ["dest_isid"]
        verbose_name = "SPB IPVPN Redistribution"
        verbose_name_plural = "SPB IPVPN Redistributions"

    def __str__(self):
        return f"Redist {self.source_vrf or self.source_isid} -> ISID {self.dest_isid.isid}"
    
    def get_absolute_url(self):
        return reverse("plugins:nautobot_spb:spb_ipvpn_redist", kwargs={"pk": self.pk})
