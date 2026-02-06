# nautobot_spb/navigation.py

from nautobot.apps.ui import NavMenuTab, NavMenuGroup, NavMenuItem, NavMenuAddButton

menu_items = (
    NavMenuTab(
        name="SPB",
        groups=(
            # === Topology ===
            NavMenuGroup(
                name="Topology",
                items=(
                    NavMenuItem(
                        link="plugins:nautobot_spb:spb_topology_list",
                        name="SPB Topologies",
                        permissions=["nautobot_spb.view_spb_topology"],
                        buttons=(NavMenuAddButton(link="plugins:nautobot_spb:spb_topology_add"),),
                    ),
                ),
            ),

            # === Backbone ===
            NavMenuGroup(
                name="Backbone",
                items=(
                    NavMenuItem(
                        link="plugins:nautobot_spb:spb_bvlan_list",
                        name="BVLANs",
                        permissions=["nautobot_spb.view_spb_bvlan"],
                        buttons=(NavMenuAddButton(link="plugins:nautobot_spb:spb_bvlan_add"),),
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_spb:spb_interface_list",
                        name="SPB Interfaces",
                        permissions=["nautobot_spb.view_spb_interface"],
                        buttons=(NavMenuAddButton(link="plugins:nautobot_spb:spb_interface_add"),),
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_spb:spb_isis_list",
                        name="SPB ISIS",
                        permissions=["nautobot_spb.view_spb_isis"],
                        buttons=(NavMenuAddButton(link="plugins:nautobot_spb:spb_isis_add"),),
                    ),
                ),
            ),

            # === Layer 2 ===
            NavMenuGroup(
                name="Layer 2",
                items=(
                    NavMenuItem(
                        link="plugins:nautobot_spb:spb_service_list",
                        name="SPB Services",
                        permissions=["nautobot_spb.view_spb_service"],
                        buttons=(NavMenuAddButton(link="plugins:nautobot_spb:spb_service_add"),),
                    ),
                ),
            ),

            # === Layer 3 ===
            NavMenuGroup(
                name="Layer 3",
                items=(
                    #NavMenuItem(
                    #    link="plugins:nautobot_spb:spb_sdp_list",
                    #    name="SDPs",
                    #    permissions=["nautobot_spb.view_spb_sdp"],
                    #    buttons=(NavMenuAddButton(link="plugins:nautobot_spb:spb_sdp_add"),),
                    #),
                    NavMenuItem(
                        link="plugins:nautobot_spb:spb_ipvpn_bind_list",
                        name="IPVPN Bindings",
                        permissions=["nautobot_spb.view_spb_ipvpn_bind"],
                        buttons=(NavMenuAddButton(link="plugins:nautobot_spb:spb_ipvpn_bind_add"),),
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_spb:spb_ipvpn_redist_list",
                        name="IPVPN Redistributions",
                        permissions=["nautobot_spb.view_spb_ipvpn_redist"],
                        buttons=(NavMenuAddButton(link="plugins:nautobot_spb:spb_ipvpn_redist_add"),),
                    ),
                ),
            ),


            NavMenuGroup(
                name="SAPs",
                items=(
                    NavMenuItem(
                        link="plugins:nautobot_spb:spb_sap_list",
                        name="SAPs",
                        permissions=["nautobot_spb.view_spb_sap"],
                        buttons=(NavMenuAddButton(link="plugins:nautobot_spb:spb_sap_add"),),
                    ),
                    #NavMenuItem(
                    #    link="plugins:nautobot_spb:spb_sdp_list",
                    #    name="SDPs",
                    #    permissions=["nautobot_spb.view_spb_sdp"],
                    #    buttons=(NavMenuAddButton(link="plugins:nautobot_spb:spb_sdp_add"),),
                    #),
                    ),
                ),
        ),
    ),
)

