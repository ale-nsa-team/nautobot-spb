from nautobot.apps.ui import NavMenuItem, NavMenuGroup, NavMenuTab
from nautobot.apps.ui import NavMenuAddButton, NavMenuImportButton

menu_items = [
    NavMenuTab(
        name="SPB",
        weight=1000,
        groups=(
            NavMenuGroup(
                name="Topology",
                weight=100,
                items=(
                    NavMenuItem(
                        link="plugins:nautobot_spb:spb_bvlan_list",
                        name="BVLANs",
                        weight=100,
                        buttons=(NavMenuAddButton(),),
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_spb:spb_service_list",
                        name="Services",
                        weight=200,
                        buttons=(NavMenuAddButton(),),
                    ),
                ),
            ),
            NavMenuGroup(
                name="Interfaces & ISIS",
                weight=200,
                items=(
                    NavMenuItem(
                        link="plugins:nautobot_spb:spb_interface_list",
                        name="SPB Interfaces",
                        weight=100,
                        buttons=(NavMenuAddButton(),),
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_spb:spb_isis_list",
                        name="ISIS Instances",
                        weight=200,
                        buttons=(NavMenuAddButton(),),
                    ),
                ),
            ),
            NavMenuGroup(
                name="IPVPN",
                weight=300,
                items=(
                    NavMenuItem(
                        link="plugins:nautobot_spb:spb_ipvpn_bind_list",
                        name="IPVPN Bindings",
                        weight=100,
                        buttons=(NavMenuAddButton(),),
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_spb:spb_ipvpn_redist_list",
                        name="IPVPN Redistribution",
                        weight=200,
                        buttons=(NavMenuAddButton(),),
                    ),
                ),
            ),
        ),
    ),
]

