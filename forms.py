# nautobot_spb/forms.py
from django import forms
from nautobot.apps.forms import (
    NautobotModelForm,
    NautobotFilterForm,
    CSVModelForm,
    StaticSelect2,
    StaticSelect2Multiple,
    DynamicModelChoiceField,
    APISelectMultiple,
    DynamicModelMultipleChoiceField,
)
from nautobot.dcim.models import Device, Interface
from nautobot.ipam.models import VRF
from . import models
from django.core.validators import RegexValidator
from django.forms import inlineformset_factory
from django.forms import modelformset_factory


# ======================================================================
# BVLAN Forms
# ======================================================================
class SPBBVLANForm(NautobotModelForm):
    """Form for creating or editing SPB BVLANs."""

    class Meta:
        model = models.SPB_BVLAN
        fields = [
            "bvlan_id",
            "name",
            "admin_state",
            "ect_id",
            "tandem_multicast_mode",
            "control",
            "description",
        ]


class SPBBVLANFilterForm(NautobotFilterForm):
    """Filter form for BVLAN list view."""

    model = models.SPB_BVLAN
    bvlan_id = forms.IntegerField(required=False, label="BVLAN ID")
    name = forms.CharField(required=False)
    admin_state = forms.NullBooleanField(required=False, label="Admin State")


# ======================================================================
# SPB Service Forms
# ======================================================================
class SPBServiceForm(NautobotModelForm):
    """Form for SPB Services."""

    # Permettre la sélection multiple de devices
    devices = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=True,
        label="Devices",
        help_text="Select one or more devices for this service"
    )
    
    bvlan = DynamicModelChoiceField(queryset=models.SPB_BVLAN.objects.all())

    class Meta:
        model = models.SPB_Service
        fields = [
            "devices",  # Au lieu de "device"
            "service_id",
            "isid",
            "bvlan",
            "pseudo_wire",
            "e_tree",
            "multicast_mode",
            "vlan_xlation",
            "stats_enabled",
            "admin_state",
            "description",
        ]

    def save(self, commit=True):
        """Create a separate service instance for each selected device."""
        devices = self.cleaned_data.get('devices', [])
        instances = []
        
        # Pour chaque device sélectionné, créer une instance de service
        for device in devices:
            instance = models.SPB_Service(
                device=device,
                service_id=self.cleaned_data['service_id'],
                isid=self.cleaned_data['isid'],
                bvlan=self.cleaned_data['bvlan'],
                pseudo_wire=self.cleaned_data['pseudo_wire'],
                e_tree=self.cleaned_data['e_tree'],
                multicast_mode=self.cleaned_data['multicast_mode'],
                vlan_xlation=self.cleaned_data['vlan_xlation'],
                stats_enabled=self.cleaned_data['stats_enabled'],
                admin_state=self.cleaned_data['admin_state'],
                description=self.cleaned_data['description'],
            )
            if commit:
                instance.save()
            instances.append(instance)
        
        return instances[0] if instances else None  # Retourner la première instance


class SPBServiceFilterForm(NautobotFilterForm):
    """Filter form for SPB Services."""

    model = models.SPB_Service
    service_id = forms.IntegerField(required=False, label="Service ID")
    isid = forms.IntegerField(required=False, label="ISID")
    device = DynamicModelChoiceField(queryset=Device.objects.all(), required=False)
    bvlan = DynamicModelChoiceField(queryset=models.SPB_BVLAN.objects.all(), required=False)


# ======================================================================
# SPB SAP Forms
# ======================================================================
# ======================================================================
# SPB SAP Forms
# ======================================================================
class SPBSAPForm(NautobotModelForm):
    """Form for creating SAPs with multiple devices, interfaces, and encapsulations."""

    service = DynamicModelChoiceField(
        queryset=models.SPB_Service.objects.all(),
        required=True,
        label="Service",
    )

    devices = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=True,
        label="Devices",
        help_text="Select one or more devices for this SAP"
    )

    interfaces = DynamicModelMultipleChoiceField(
        queryset=Interface.objects.all(),
        required=True,
        label="Interfaces",
        help_text="Select one or more interfaces"
    )

    encapsulation = forms.CharField(
        required=True,
        label="Encapsulation(s)",
        help_text="Comma-separated encapsulations (e.g., :0, :10, :20)",
        widget=forms.TextInput(attrs={
            'placeholder': ':0, :10, :20'
        })
    )

    admin_state = forms.BooleanField(
        required=False,
        initial=True,
        label="Admin State"
    )

    class Meta:
        model = models.SPB_SAP
        fields = ["service", "devices", "interfaces", "encapsulation", "admin_state"]

    def clean_encapsulation(self):
        """Validate and clean encapsulation input."""
        encap_str = self.cleaned_data.get("encapsulation", "")

        # Split by comma and clean whitespace
        encaps = [e.strip() for e in encap_str.split(",") if e.strip()]

        if not encaps:
            raise forms.ValidationError("At least one encapsulation is required.")

        # Validate format (should start with :)
        for encap in encaps:
            if not encap.startswith(":"):
                raise forms.ValidationError(
                    f"Invalid encapsulation format: '{encap}'. Must start with ':' (e.g., :0, :10)"
                )

        return encaps  # Return as list

    def save(self, commit=True):
        """Create a SAP for each device-interface-encapsulation combination."""
        service = self.cleaned_data["service"]
        devices = self.cleaned_data["devices"]
        interfaces = self.cleaned_data["interfaces"]
        encapsulations = self.cleaned_data["encapsulation"]  # Already a list from clean_encapsulation
        admin_state = self.cleaned_data.get("admin_state", True)

        instances = []

        for device in devices:
            for interface in interfaces:
                # Check if interface belongs to the device
                #if interface.device != device:
                #    continue  # Skip interfaces that don't belong to this device
                if interface.device != device:
                    raise forms.ValidationError(
                        f"Interface {interface.name} belongs to {interface.device.name}. "
                        f"Please select an interface matching the selected device(s)."
                    )

                # Check if SAP already exists for this combination
                existing = models.SPB_SAP.objects.filter(
                    service=service,
                    device=device,
                    interface=interface
                ).first()

                if existing:
                    # Merge encapsulations (add new ones, avoid duplicates)
                    current_encaps = existing.encapsulation if isinstance(existing.encapsulation, list) else []
                    new_encaps = list(set(current_encaps + encapsulations))
                    existing.encapsulation = new_encaps
                    existing.admin_state = admin_state
                    if commit:
                        existing.save()
                    instances.append(existing)

                else:
                    # Create new SAP
                    sap = models.SPB_SAP(
                        service=service,
                        device=device,
                        interface=interface,
                        encapsulation=encapsulations,
                        admin_state=admin_state
                    )
                    if commit:
                        sap.save()
                    instances.append(sap)

        return instances[0] if instances else None



#======================================================================
# SPB SDP Forms
# ======================================================================
class SPBSDPForm(NautobotModelForm):
    """Form for SPB SDPs."""

    bvlan = DynamicModelChoiceField(queryset=models.SPB_BVLAN.objects.all())

    class Meta:
        model = models.SPB_SDP
        fields = [
            "sdp_id",
            "sysid",
            "bvlan",
            "source_id",
            "oper_state",
            "dynamic",
            "bind_count",
        ]



# ======================================================================
# SPB Interface Forms
# ======================================================================
class SPBInterfaceForm(NautobotModelForm):
    """Form for SPB Interfaces."""

    device = DynamicModelChoiceField(queryset=Device.objects.all())
    interface = DynamicModelChoiceField(queryset=Interface.objects.all())
    bvlan = DynamicModelChoiceField(queryset=models.SPB_BVLAN.objects.all())
    class Meta:
        model = models.SPB_Interface
        fields = [
            "device",
            "interface",
            "bvlan",
            "iface_type",
            "hello_interval",
            "hello_multiplier",
            "metric",
            "priority",
            "admin_state",
        ]


# ======================================================================
# SPB ISIS Forms
# ======================================================================
class SPBISISForm(NautobotModelForm):
    """Form for SPB ISIS instances."""

    device = DynamicModelChoiceField(queryset=Device.objects.all())
    bvlan = DynamicModelChoiceField(
        queryset=models.SPB_BVLAN.objects.filter(control=True),
        required=True,
        label="Control BVLAN",
    )

    class Meta:
        model = models.SPB_ISIS
        fields = [
            "device",
            "bvlan",
            "bridge_priority",
            "spf_wait",
            "lsp_wait",
            "graceful_restart",
        ]


class SPBISISFilterForm(NautobotFilterForm):
    """Filter form for SPB ISIS instances."""

    model = models.SPB_ISIS
    device = DynamicModelChoiceField(queryset=Device.objects.all(), required=False)
    bvlan = DynamicModelChoiceField(queryset=models.SPB_BVLAN.objects.filter(control=True), required=False)


# ======================================================================
# SPB IPVPN Bind Forms
# ======================================================================
class SPBIPVPNBindForm(NautobotModelForm):
    """Form for SPB IPVPN Bindings."""

    vrf = DynamicModelChoiceField(queryset=VRF.objects.all())
    service = DynamicModelChoiceField(queryset=models.SPB_Service.objects.all())

    class Meta:
        model = models.SPB_IPVPN_Bind
        fields = [
            "vrf",
            "service",
            "gateway",
            "import_route_map",
            "all_routes",
        ]


# ======================================================================
# SPB IPVPN Redistribution Forms
# ======================================================================
class SPBIPVPNRedistForm(NautobotModelForm):
    """Form for SPB IPVPN Redistributions."""

    source_vrf = DynamicModelChoiceField(queryset=VRF.objects.all(), required=False)
    source_isid = DynamicModelChoiceField(queryset=models.SPB_Service.objects.all(), required=False)
    dest_isid = DynamicModelChoiceField(queryset=models.SPB_Service.objects.all())

    class Meta:
        model = models.SPB_IPVPN_Redist
        fields = [
            "source_vrf",
            "source_isid",
            "dest_isid",
            "route_map",
            "all_routes",
        ]


# ======================================================================
# CSV Import Forms
# ======================================================================
class SPBBVLANCSVForm(CSVModelForm):
    """CSV import form for BVLANs."""

    class Meta:
        model = models.SPB_BVLAN
        fields = [
            "bvlan_id",
            "name",
            "admin_state",
            "ect_id",
            "tandem_multicast_mode",
            "control",
            "description",
        ]


class SPBServiceCSVForm(CSVModelForm):
    """CSV import form for SPB Services."""

    bvlan = forms.ModelChoiceField(
        queryset=models.SPB_BVLAN.objects.all(),
        to_field_name="bvlan_id",
    )

    class Meta:
        model = models.SPB_Service
        fields = [
            "service_id",
            "isid",
            "bvlan",
            "pseudo_wire",
            "e_tree",
            "multicast_mode",
            "admin_state",
        ]









class SPBTopologyForm(NautobotModelForm):
    """Form for creating/editing SPB Topologies with tag-style multi-select."""

    # === Control BVLAN - Simple number input ===
    control_bvlan_id = forms.IntegerField(
        required=True,
        label="Control BVLAN",
        help_text="Select one Control BVLAN (unique per topology).",
        min_value=1000,
        max_value=4999,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )

    # === Data BVLANs - Multi-select like Devices ===
    data_bvlan_ids = forms.MultipleChoiceField(
        required=False,
        label="Data BVLAN IDs",
        help_text="Select one or more Data BVLANs, excluding the Control BVLAN.",
        choices=[(str(i), str(i)) for i in range(1000, 5000)],
        widget=StaticSelect2Multiple(attrs={
            "data-placeholder": "Select Data BVLANs...",
        }),
    )

    # === Devices - Multi-select with API integration ===
    devices = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        label="Devices",
        help_text="Select devices for this SPB topology.",
    )

    # === Existing SPB Interfaces - Multi-select ===
    related_interfaces = DynamicModelMultipleChoiceField(
        queryset=Interface.objects.all(),
        required=False,
        label="Interfaces",
        help_text="Select physical interfaces from devices participating in this topology.",
        widget=APISelectMultiple(
            api_url="/api/dcim/interfaces/",
        ),
    )   

    # === SPB Interface Configuration Fields ===
    IFACE_TYPE_CHOICES = [
        ("", "----------"),
        ("p2p", "Point-to-Point"),
        ("multi-access", "Multi-Access"),
    ]

    topology_interface_type = forms.ChoiceField(
        choices=IFACE_TYPE_CHOICES,
        required=False,
        initial="multi-access",
        label="Interface Type",
        help_text="Default interface type for this topology",
        widget=StaticSelect2(attrs={"class": "form-control"}),
    )

    topology_hello_interval = forms.IntegerField(
        required=False,
        label="Hello Interval (ms)",
        help_text="Default hello interval in milliseconds",
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "Hello Interval (s)"
        }),
    )

    topology_hello_multiplier = forms.IntegerField(
        required=False,
        label="Hello Multiplier",
        help_text="Default hello multiplier",
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "Hello Multiplier"
        }),
    )

    topology_metric = forms.IntegerField(
        required=False,
        label="Metric",
        help_text="Default metric for interfaces",
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "Metric"
        }),
    )

    topology_priority = forms.IntegerField(
        required=False,
        label="Priority",
        help_text="Default priority for interfaces",
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "Priority not needed in Point-to-Point"
        }),
    )

    topology_admin_state = forms.BooleanField(
        required=False,
        initial=True,
        label="Admin State",
        help_text="Default admin state for interfaces",
    )

    class Meta:
        model = models.SPB_Topology
        fields = [
            "name",
            "description",
            "control_bvlan_id",
            "data_bvlan_ids",
            "devices",
            "related_interfaces",
            "topology_interface_type",
            "topology_hello_interval",
            "topology_hello_multiplier",
            "topology_metric",
            "topology_priority",
            "topology_admin_state",
        ]

    # Define fieldsets for visual separation
    fieldsets = (
        ("SPB Topology", {
            "fields": (
                "name",
                "description",
                "control_bvlan_id",
                "data_bvlan_ids",
                "devices",
                "related_interfaces",
            ),
        }),
        ("SPB Interface Configuration", {
            "fields": (
                "topology_interface_type",
                "topology_hello_interval",
                "topology_hello_multiplier",
                "topology_metric",
                "topology_priority",
                "topology_admin_state",
            ),
            "description": "Configure default SPB interface settings for this topology",
        }),
    )

    def __init__(self, *args, **kwargs):
        """Initialize form and handle data_bvlan_ids conversion."""
        super().__init__(*args, **kwargs)
        
        # If editing an existing topology, convert string to list for the widget
        if self.instance and self.instance.pk and self.instance.data_bvlan_ids:
            # Convert comma-separated string to list of strings
            bvlan_list = [x.strip() for x in self.instance.data_bvlan_ids.split(",") if x.strip()]
            self.initial['data_bvlan_ids'] = bvlan_list
        
    def clean(self):
        """Validate BVLAN fields and ensure topology name is not empty."""
        super().clean()  # Appelle la validation de base

        # --- Ensure name is valid ---
        name = self.cleaned_data.get("name")
        if not name or not name.strip():
            self.add_error("name", "Please provide a valid name for this topology.")
        else:
            # Nettoie le nom (supprime espaces inutiles)
            self.cleaned_data["name"] = name.strip()

        # --- Control vs Data BVLAN check ---
        control_bvlan = self.cleaned_data.get("control_bvlan_id")
        data_bvlans = self.cleaned_data.get("data_bvlan_ids") or []

        if control_bvlan and str(control_bvlan) in [str(v) for v in data_bvlans]:
            self.add_error(
                "data_bvlan_ids",
                f"BVLAN {control_bvlan} cannot be both Control and Data BVLAN."
            )

    def save(self, commit=True):
        """Convert list back to comma-separated string for database storage."""
        instance = super().save(commit=False)

        data_bvlans = self.cleaned_data.get("data_bvlan_ids") or []
        instance.data_bvlan_ids = ",".join(map(str, data_bvlans))

        if commit:
            instance.save()
            self.save_m2m()  # This saves the many-to-many relationships
        
            # **NEW: Update cached fields AFTER m2m relationships are saved**
            instance.cached_devices = [d.name for d in instance.devices.all()]
            instance.cached_interfaces = [
                f"{i.device.name}:{i.name}" for i in instance.related_interfaces.all()
            ]
            # Save again with update_fields to trigger webhook with populated data
            instance.save(update_fields=["cached_devices", "cached_interfaces"])

        return instance
