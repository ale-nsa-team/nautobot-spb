# nautobot_spb/models.py
from django.db import models
from django.urls import reverse
from nautobot.apps.models import PrimaryModel
from nautobot.dcim.models import Device, Interface
from nautobot.ipam.models import VRF
from nautobot.extras.utils import extras_features
from nautobot.core.models.querysets import RestrictedQuerySet
from django.core.exceptions import ValidationError
from django.db.models import JSONField
# =====================================================================
# SPB BVLAN
# =====================================================================
@extras_features("webhooks")
class SPB_BVLAN(PrimaryModel):
    bvlan_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    admin_state = models.BooleanField(default=True)
    ect_id = models.PositiveSmallIntegerField(blank=True, null=True)
    tandem_multicast_mode = models.CharField(
        max_length=8,
        choices=(("sgmode", "sgmode"), ("gmode", "gmode")),
        default="sgmode"
    )
    control = models.BooleanField(default=False)
    description = models.CharField(max_length=200, blank=True)

    objects = RestrictedQuerySet.as_manager()

    def clean(self):
        """Ensure unique control BVLAN and unique ECT-ID."""
        from django.core.exceptions import ValidationError
        super().clean()

        # Only one control BVLAN allowed
        if self.control:
            existing = SPB_BVLAN.objects.filter(control=True).exclude(pk=self.pk)
            if existing.exists():
                raise ValidationError({"control": "Only one control BVLAN is allowed."})

        # ECT-ID must be unique
        if self.ect_id is not None:
            duplicate = SPB_BVLAN.objects.filter(ect_id=self.ect_id).exclude(pk=self.pk)
            if duplicate.exists():
                raise ValidationError({"ect_id": f"ECT-ID {self.ect_id} is already used."})

    def save(self, *args, **kwargs):
        """Prevent modification of the control BVLAN and auto-create ISIS if control=True."""
        from django.core.exceptions import ValidationError
        creating = self._state.adding

        # Prevent modification of existing control BVLAN
        if not creating:
            existing = SPB_BVLAN.objects.get(pk=self.pk)
            if existing.control and (
                self.bvlan_id != existing.bvlan_id
                or self.name != existing.name
                or self.ect_id != existing.ect_id
                or self.tandem_multicast_mode != existing.tandem_multicast_mode
                or self.description != existing.description
            ):
                raise ValidationError("The control BVLAN cannot be modified.")

        # Only one control BVLAN in the infra
        if creating and self.control and SPB_BVLAN.objects.filter(control=True).exists():
            raise ValidationError("A control BVLAN already exists — cannot create another.")

        super().save(*args, **kwargs)

        # Auto-create ISIS-SPB if this is the control BVLAN and none exists
        if self.control and not hasattr(self, "isis_config"):
            SPB_ISIS.objects.create(bvlan=self, device=Device.objects.first())

    def delete(self, *args, **kwargs):
        from django.core.exceptions import ValidationError
        if self.control:
            raise ValidationError("The control BVLAN cannot be deleted.")
        super().delete(*args, **kwargs)

    class Meta:
        ordering = ["bvlan_id"]
        verbose_name = "SPB BVLAN"
        verbose_name_plural = "SPB BVLANs"

    def __str__(self):
        return f"BVLAN {self.bvlan_id} {self.name or ''}"

    def get_absolute_url(self):
        return reverse("plugins:nautobot_spb:spb_bvlan", kwargs={"pk": self.pk})


# =====================================================================
# SPB Service
# =====================================================================
@extras_features("webhooks")
class SPB_Service(PrimaryModel):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    service_id = models.PositiveIntegerField()  # Retirer unique=True
    isid = models.PositiveIntegerField()
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

    objects = RestrictedQuerySet.as_manager()

    class Meta:
        ordering = ["service_id"]
        # Modifier unique_together pour permettre même ISID/BVLAN sur différents devices
        unique_together = (("device", "service_id"), ("device", "isid", "bvlan"))
        verbose_name = "SPB Service"
        verbose_name_plural = "SPB Services"

    def __str__(self):
        return f"SPB Service {self.service_id} (ISID {self.isid}) on {self.device}"

    def get_absolute_url(self):
        return reverse("plugins:nautobot_spb:spb_service", kwargs={"pk": self.pk})
# =====================================================================
# SPB SAP
# =====================================================================
@extras_features("webhooks")
class SPB_SAP(PrimaryModel):
    service = models.ForeignKey(SPB_Service, on_delete=models.CASCADE, related_name="saps")
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    interface = models.ForeignKey(Interface, on_delete=models.CASCADE)
    encapsulation = models.JSONField(default=list, blank=True)
    admin_state = models.BooleanField(default=True)

    objects = RestrictedQuerySet.as_manager()

    class Meta:
        ordering = ["device", "interface"]
        verbose_name = "SPB SAP"
        verbose_name_plural = "SPB SAPs"

    def __str__(self):
        encaps = ", ".join(self.encapsulation) if isinstance(self.encapsulation, list) else self.encapsulation
        return f"SAP {self.device}:{self.interface} (Service {self.service.service_id}) [{encaps}]"

    def get_absolute_url(self):
        return reverse("plugins:nautobot_spb:spb_sap", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        # Ensure encapsulation is a list
        if not isinstance(self.encapsulation, list):
            if self.encapsulation:
                self.encapsulation = [self.encapsulation]
            else:
                self.encapsulation = [":0"]  # Default encapsulation
        super().save(*args, **kwargs)
#=====================================================================
# SPB SDP
# =====================================================================
@extras_features("webhooks")
class SPB_SDP(PrimaryModel):
    sdp_id = models.PositiveIntegerField()
    sysid = models.CharField(max_length=32)
    bvlan = models.ForeignKey(SPB_BVLAN, on_delete=models.CASCADE)
    source_id = models.CharField(max_length=32, blank=True, null=True)
    oper_state = models.CharField(max_length=16, blank=True)
    dynamic = models.BooleanField(default=True)
    bind_count = models.PositiveIntegerField(default=0)

    objects = RestrictedQuerySet.as_manager()

    class Meta:
        ordering = ["sdp_id"]
        verbose_name = "SPB SDP"
        verbose_name_plural = "SPB SDPs"

    def __str__(self):
        return f"SDP {self.sdp_id} ({self.sysid}:{self.bvlan.bvlan_id})"

    def get_absolute_url(self):
        return reverse("plugins:nautobot_spb:spb_sdp", kwargs={"pk": self.pk})


# =====================================================================
# SPB Interface
# =====================================================================
@extras_features("webhooks")
class SPB_Interface(PrimaryModel):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    interface = models.ForeignKey(Interface, on_delete=models.CASCADE)
    bvlan = models.ForeignKey(SPB_BVLAN, on_delete=models.CASCADE)
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

    objects = RestrictedQuerySet.as_manager()

    class Meta:
        ordering = ["device", "interface"]
        unique_together = ("device", "interface")
        verbose_name = "SPB Interface"
        verbose_name_plural = "SPB Interfaces"

    def __str__(self):
        return f"{self.device}:{self.interface} (SPB)"

    def get_absolute_url(self):
        return reverse("plugins:nautobot_spb:spb_interface", kwargs={"pk": self.pk})


# =====================================================================
# SPB ISIS
# =====================================================================
@extras_features("webhooks")
class SPB_ISIS(PrimaryModel):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    bvlan = models.OneToOneField(
        "SPB_BVLAN",
        on_delete=models.CASCADE,
        related_name="isis_config",
        limit_choices_to={"control": True},
    )
    bridge_priority = models.PositiveIntegerField(default=32768)
    spf_wait = models.PositiveIntegerField(default=50, blank=True, null=True)
    lsp_wait = models.PositiveIntegerField(default=100, blank=True, null=True)
    graceful_restart = models.BooleanField(default=False)

    class Meta:
        ordering = ["device"]
        verbose_name = "SPB ISIS Instance"
        verbose_name_plural = "SPB ISIS Instances"

    def __str__(self):
        return f"ISIS-SPB on {self.device} (BVLAN {self.bvlan.bvlan_id})"


# =====================================================================
# SPB IPVPN Bind
# =====================================================================
@extras_features("webhooks")
class SPB_IPVPN_Bind(PrimaryModel):
    vrf = models.ForeignKey(VRF, on_delete=models.CASCADE)
    service = models.ForeignKey(SPB_Service, on_delete=models.CASCADE)
    gateway = models.GenericIPAddressField()
    import_route_map = models.CharField(max_length=128, blank=True)
    all_routes = models.BooleanField(default=False)

    objects = RestrictedQuerySet.as_manager()

    class Meta:
        ordering = ["vrf", "service"]
        unique_together = ("vrf", "service")
        verbose_name = "SPB IPVPN Binding"
        verbose_name_plural = "SPB IPVPN Bindings"

    def __str__(self):
        return f"IPVPN bind VRF {self.vrf} <-> ISID {self.service.isid}"

    def get_absolute_url(self):
        return reverse("plugins:nautobot_spb:spb_ipvpn_bind", kwargs={"pk": self.pk})


# =====================================================================
# SPB IPVPN Redist
# =====================================================================
@extras_features("webhooks")
class SPB_IPVPN_Redist(PrimaryModel):
    source_vrf = models.ForeignKey(VRF, on_delete=models.SET_NULL, blank=True, null=True)
    source_isid = models.ForeignKey(
        SPB_Service,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="redist_sources"
    )
    dest_isid = models.ForeignKey(
        SPB_Service,
        on_delete=models.CASCADE,
        related_name="redist_dest"
    )
    route_map = models.CharField(max_length=128, blank=True)
    all_routes = models.BooleanField(default=False)

    objects = RestrictedQuerySet.as_manager()

    class Meta:
        ordering = ["dest_isid"]
        verbose_name = "SPB IPVPN Redistribution"
        verbose_name_plural = "SPB IPVPN Redistributions"

    def __str__(self):
        return f"Redist {self.source_vrf or self.source_isid} -> ISID {self.dest_isid.isid}"

    def get_absolute_url(self):
        return reverse("plugins:nautobot_spb:spb_ipvpn_redist", kwargs={"pk": self.pk})

# =======================================================================
# SPB Topology
# =======================================================================

@extras_features("webhooks")
class SPB_Topology(PrimaryModel):
    """
    SPB Topology model with integrated SPB Interface configuration
    """
    # Existing fields
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255, blank=True)
    control_bvlan_id = models.PositiveIntegerField(
        help_text="Control BVLAN (unique per topology).",
        default=1000,
    )
    data_bvlan_ids = models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma-separated list of Data BVLAN IDs (e.g., 2001,2002,2003).",
    )
    devices = models.ManyToManyField(
        Device,
        blank=True,
        related_name="spb_topologies",
        help_text="Select devices participating in this SPB topology.",
    )
    #related_interfaces = models.ManyToManyField(
    #    "SPB_Interface",
    #    blank=True,
    #    related_name="related_topologies",
    #    help_text="SPB interfaces shown in this topology form.",
    #)
        
    related_interfaces = models.ManyToManyField(
        "dcim.Interface",
        blank=True,
        related_name="spb_topologies",
        help_text="Physical interfaces linked to this topology.",
    )


    # === NEW: SPB Interface Configuration Fields ===
    topology_interface_type = models.CharField(
        max_length=12,
        choices=(("p2p", "p2p"), ("multi-access", "multi-access")),
        default="p2p",
        help_text="Default interface type for this topology"
    )
    topology_hello_interval = models.PositiveIntegerField(
        blank=True, 
        null=True,
        default=9,
        help_text="Default hello interval (ms)"
    )
    topology_hello_multiplier = models.PositiveIntegerField(
        blank=True, 
        null=True,
        default=3,
        help_text="Default hello multiplier"

    )
    topology_metric = models.PositiveSmallIntegerField(
        blank=True, 
        null=True,
        default=10,
        help_text="Default metric for interfaces"
    )
    topology_priority = models.PositiveIntegerField(
        blank=True, 
        null=True,
        help_text="Default priority for interfaceis ( is not needed in P2P )"
    )
    topology_admin_state = models.BooleanField(
        default=True,
        help_text="Default admin state for interfaces"
    )
    # === Helpers for Webhooks ===
    @property
    def device_list(self):
        """Return list of device names (for webhooks)."""
        return [device.name for device in self.devices.all()]

    @property
    def interface_list(self):
        """Return list of interfaces as 'Device:Interface' (for webhooks)."""
        return [f"{iface.device.name}:{iface.name}" for iface in self.related_interfaces.all()]
    
    #test

    cached_devices = JSONField(default=list, blank=True)
    cached_interfaces = JSONField(default=list, blank=True)
    
    def save(self, *args, **kwargs):
    # Ensure BVLANs listed in data_bvlan_ids exist as SPB_BVLAN objects
        from nautobot_spb.models import SPB_BVLAN

        if self.data_bvlan_ids:
            data_ids = [int(x.strip()) for x in self.data_bvlan_ids.split(",") if x.strip()]

            for bvlan_id in data_ids:
                # Check if already exists, if not create
                if not SPB_BVLAN.objects.filter(bvlan_id=bvlan_id).exists():
                    SPB_BVLAN.objects.create(
                        bvlan_id=bvlan_id,
                        name=f"auto_data_{bvlan_id}",
                        admin_state=True,
                        control=False,
                        description="Auto-created Data BVLAN from SPB Topology"
                    )

        # Control BVLAN auto creation
        if self.control_bvlan_id:
            ctrl = int(self.control_bvlan_id)
            if not SPB_BVLAN.objects.filter(bvlan_id=ctrl).exists():
                SPB_BVLAN.objects.create(
                    bvlan_id=ctrl,
                    name=f"ctrl_bvlan_{ctrl}",
                    admin_state=True,
                    control=True,
                    description="Auto-created Control BVLAN from SPB Topology"
                )

        # Standard save
        super().save(*args, **kwargs)
    def clean(self):
        """Validation logic"""
        if self.data_bvlan_ids:
            data_ids = [x.strip() for x in self.data_bvlan_ids.split(",") if x.strip()]
            if str(self.control_bvlan_id) in data_ids:
                raise ValidationError("The control BVLAN cannot be included in the data BVLAN list.")

        #if SPB_Topology.objects.exclude(pk=self.pk).exists():
            #raise ValidationError("Only one SPB Topology instance is allowed.")

    class Meta:
        ordering = ["name"]
        verbose_name = "SPB Topology"
        verbose_name_plural = "SPB Topologies"

    def __str__(self):
        return f"{self.name} (Ctrl BVLAN {self.control_bvlan_id})"

    def get_absolute_url(self):
        return reverse("plugins:nautobot_spb:spb_topology", kwargs={"pk": self.pk})
