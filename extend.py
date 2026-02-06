# nautobot_spb/extend.py
"""
UI extensions for SPB plugin - registers additional tabs on Device and Interface pages.
"""
from nautobot.apps.ui import TemplateExtension
from .models import SPB_Interface, SPB_SAP, SPB_ISIS


class DeviceSPBISIS(TemplateExtension):
    """Add SPB ISIS tab to Device detail view."""
    
    model = "dcim.device"

    def detail_tabs(self):
        spb_isis = SPB_ISIS.objects.filter(device=self.context["object"]).first()
        return [
            {
                "title": "SPB ISIS",
                "url": f"plugins:nautobot_spb:spb_isis?device_id={self.context['object'].pk}",
            }
        ]


class DeviceSPBInterfaces(TemplateExtension):
    """Add SPB Interfaces tab to Device detail view."""
    
    model = "dcim.device"

    def detail_tabs(self):
        return [
            {
                "title": "SPB Interfaces",
                "url": f"plugins:nautobot_spb:spb_interface_list?device_id={self.context['object'].pk}",
            }
        ]


class DeviceSPBServices(TemplateExtension):
    """Add SPB Services (SAPs) tab to Device detail view."""
    
    model = "dcim.device"

    def detail_tabs(self):
        return [
            {
                "title": "SPB Services",
                "url": f"plugins:nautobot_spb:spb_sap_list?device_id={self.context['object'].pk}",
            }
        ]


class InterfaceSPBConfig(TemplateExtension):
    """Add SPB Interface Config tab to Interface detail view."""
    
    model = "dcim.interface"

    def detail_tabs(self):
        spb_interface = SPB_Interface.objects.filter(interface=self.context["object"]).first()
        return [
            {
                "title": "SPB Config",
                "url": f"plugins:nautobot_spb:spb_interface_list?interface_id={self.context['object'].pk}",
            }
        ]


# Register all extensions
template_extensions = [
    DeviceSPBISIS,
    DeviceSPBInterfaces,
    DeviceSPBServices,
    InterfaceSPBConfig,
]
