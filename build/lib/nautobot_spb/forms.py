from nautobot.apps.forms import NautobotModelForm, NautobotBulkEditForm, NautobotFilterForm
from nautobot.utilities.forms.fields import DynamicModelChoiceField
from . import models


class SPBBVLANForm(NautobotModelForm):
    class Meta:
        model = models.SPB_BVLAN
        fields = '__all__'


class SPBBVLANFilterForm(NautobotFilterForm):
    model = models.SPB_BVLAN
    
    
class SPBServiceForm(NautobotModelForm):
    bvlan = DynamicModelChoiceField(queryset=models.SPB_BVLAN.objects.all())
    
    class Meta:
        model = models.SPB_Service
        fields = '__all__'


class SPBServiceFilterForm(NautobotFilterForm):
    model = models.SPB_Service


# Repeat for all other models...
class SPBInterfaceForm(NautobotModelForm):
    class Meta:
        model = models.SPB_Interface
        fields = '__all__'


class SPBISISForm(NautobotModelForm):
    class Meta:
        model = models.SPB_ISIS
        fields = '__all__'
