# nautobot_spb/api/urls.py
from nautobot.apps.api import OrderedDefaultRouter
from nautobot_spb.api import views

router = OrderedDefaultRouter()
router.register("spb_bvlan", views.SPBBVLANViewSet)
router.register("spb_service", views.SPBServiceViewSet)
router.register("spb_interface", views.SPBInterfaceViewSet)
router.register("spb_isis", views.SPBISISViewSet)
router.register("spb_sap", views.SPBSAPViewSet)
router.register("spb_sdp", views.SPBSDPViewSet)
router.register("spb_ipvpn_bind", views.SPBIPVPNBindViewSet)
router.register("spb_ipvpn_redist", views.SPBIPVPNRedistViewSet)

urlpatterns = router.urls

