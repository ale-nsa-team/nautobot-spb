from nautobot.apps import ui
from nautobot.dcim.models import Device, Interface
from .models import SPB_Interface, SPB_SAP, SPB_Service, SPB_ISIS


#
# Attach SPB info to the Device page
#
ui.register_model_tab(
    model=Device,
    label="SPB ISIS",
    tab_id="spb_isis",
    queryset=lambda request, obj: SPB_ISIS.objects.filter(device=obj),
)

ui.register_model_tab(
    model=Device,
    label="SPB Interfaces",
    tab_id="spb_interfaces",
    queryset=lambda request, obj: SPB_Interface.objects.filter(device=obj),
)

ui.register_model_tab(
    model=Device,
    label="SPB Services",
    tab_id="spb_services",
    queryset=lambda request, obj: SPB_SAP.objects.filter(device=obj),
)


#
# Attach SPB info to each Interface page
#
ui.register_model_tab(
    model=Interface,
    label="SPB Interface Config",
    tab_id="spb_iface",
    queryset=lambda request, obj: SPB_Interface.objects.filter(interface=obj),
)

