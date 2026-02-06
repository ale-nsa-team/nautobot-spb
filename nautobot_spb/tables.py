# nautobot_spb/tables.py
import django_tables2 as tables
from nautobot.apps.tables import BaseTable, ToggleColumn
from . import models


class SPB_BVLANTable(BaseTable):
    pk = ToggleColumn()
    bvlan_id = tables.Column(linkify=True)
    name = tables.Column()
    admin_state = tables.BooleanColumn()

    class Meta(BaseTable.Meta):
        model = models.SPB_BVLAN
        fields = ("pk", "bvlan_id", "name", "admin_state", "ect_id", "control", "description")
        default_actions = ()


class SPB_ServiceTable(BaseTable):
    pk = ToggleColumn()
    service_id = tables.Column(linkify=True)
    isid = tables.Column()
    bvlan = tables.Column(linkify=True)

    class Meta(BaseTable.Meta):
        model = models.SPB_Service
        fields = ("pk", "service_id", "isid", "bvlan", "admin_state", "multicast_mode", "description")
        default_actions = ()


#class SPB_SAPTable(BaseTable):
#    pk = ToggleColumn()
#    service = tables.Column(linkify=True)
#    device = tables.Column(linkify=True)
#    interface = tables.Column(linkify=True)

#    class Meta(BaseTable.Meta):
#        model = models.SPB_SAP
#        fields = ("pk", "service", "device", "interface", "encapsulation", "admin_state")
#        default_actions = ()
class SPB_SAPTable(BaseTable):
    pk = ToggleColumn()
    service = tables.Column(linkify=True)
    device = tables.Column(linkify=True)
    interface = tables.Column(linkify=True)
    encapsulation = tables.TemplateColumn(
        template_code="""
        {% if record.encapsulation %}
            {% for encap in record.encapsulation %}
                <span class="badge badge-secondary">{{ encap }}</span>
            {% endfor %}
        {% endif %}
        """,
        verbose_name="Encapsulations"
    )

    class Meta(BaseTable.Meta):
        model = models.SPB_SAP
        fields = ("pk", "service", "device", "interface", "encapsulation", "admin_state")
        default_actions = ()

class SPB_SDPTable(BaseTable):
    pk = ToggleColumn()
    sdp_id = tables.Column(linkify=True)
    sysid = tables.Column()
    bvlan = tables.Column(linkify=True)

    class Meta(BaseTable.Meta):
        model = models.SPB_SDP
        fields = ("pk", "sdp_id", "sysid", "bvlan", "oper_state", "dynamic", "bind_count")
        default_actions = ()


class SPB_InterfaceTable(BaseTable):
    pk = ToggleColumn()
    device = tables.Column(linkify=True)
    interface = tables.Column(linkify=True)
    iface_type = tables.Column()

    class Meta(BaseTable.Meta):
        model = models.SPB_Interface
        fields = ("pk", "device", "interface", "iface_type", "metric", "priority", "admin_state")
        default_actions = ()


class SPB_ISISTable(BaseTable):
    pk = ToggleColumn()
    device = tables.Column(linkify=True)
    bridge_priority = tables.Column()
    control_bvlan = tables.Column(linkify=True)

    class Meta(BaseTable.Meta):
        model = models.SPB_ISIS
        fields = ("pk", "device", "bridge_priority", "control_bvlan", "graceful_restart")
        default_actions = ()


class SPB_IPVPN_BindTable(BaseTable):
    pk = ToggleColumn()
    vrf = tables.Column(linkify=True)
    service = tables.Column(linkify=True)
    gateway = tables.Column()

    class Meta(BaseTable.Meta):
        model = models.SPB_IPVPN_Bind
        fields = ("pk", "vrf", "service", "gateway", "all_routes", "import_route_map")
        default_actions = ()


class SPB_IPVPN_RedistTable(BaseTable):
    pk = ToggleColumn()
    source_vrf = tables.Column(linkify=True)
    source_isid = tables.Column(linkify=True)
    dest_isid = tables.Column(linkify=True)

    class Meta(BaseTable.Meta):
        model = models.SPB_IPVPN_Redist
        fields = ("pk", "source_vrf", "source_isid", "dest_isid", "route_map", "all_routes")
        default_actions = ()

# === SPB Topology ===
class SPBTopologyTable(BaseTable):
    pk = ToggleColumn()
    name = tables.Column(linkify=True, verbose_name="Topology Name")
    control_bvlan = tables.Column(
        accessor="control_bvlan_id",
        verbose_name="Control BVLAN",
    )
    devices = tables.ManyToManyColumn(
        linkify_item=True,
        verbose_name="Devices"
    )
    data_bvlans = tables.TemplateColumn(
        template_code="""
        {% for id in record.data_bvlan_ids|cut:' '|cut:',' %}
            <span class="badge badge-info">{{ id }}</span>
        {% endfor %}
        """,
        verbose_name="Data BVLANs",
    )
    # Add new columns if you want to show interface config in table
    topology_interface_type = tables.Column(verbose_name="Default IF Type")
    topology_metric = tables.Column(verbose_name="Default Metric")

    class Meta(BaseTable.Meta):
        model = models.SPB_Topology
        fields = (
            "pk", 
            "name", 
            "control_bvlan", 
            "devices", 
            "data_bvlans",
            "topology_interface_type",
            "topology_metric",
        )
        default_actions = ("edit", "delete")
        default_columns = ("name", "control_bvlan", "devices", "data_bvlans")
