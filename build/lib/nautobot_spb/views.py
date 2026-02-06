from nautobot.apps import views
from . import models, tables, forms


# BVLAN Views
class SPBBVLANListView(views.generic.ObjectListView):
    queryset = models.SPB_BVLAN.objects.all()
    table = tables.SPB_BVLANTable
    filterset_class = forms.SPBBVLANFilterForm


class SPBBVLANView(views.generic.ObjectView):
    queryset = models.SPB_BVLAN.objects.all()


class SPBBVLANEditView(views.generic.ObjectEditView):
    queryset = models.SPB_BVLAN.objects.all()
    form_class = forms.SPBBVLANForm


class SPBBVLANDeleteView(views.generic.ObjectDeleteView):
    queryset = models.SPB_BVLAN.objects.all()


class SPBBVLANBulkDeleteView(views.generic.BulkDeleteView):
    queryset = models.SPB_BVLAN.objects.all()
    table = tables.SPB_BVLANTable


# Service Views
class SPBServiceListView(views.generic.ObjectListView):
    queryset = models.SPB_Service.objects.all()
    table = tables.SPB_ServiceTable


class SPBServiceView(views.generic.ObjectView):
    queryset = models.SPB_Service.objects.all()


class SPBServiceEditView(views.generic.ObjectEditView):
    queryset = models.SPB_Service.objects.all()
    form_class = forms.SPBServiceForm


class SPBServiceDeleteView(views.generic.ObjectDeleteView):
    queryset = models.SPB_Service.objects.all()


# Repeat similar pattern for all other models...
