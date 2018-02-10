import django_filters

from .models import GVAIncident


class GVAIncidentFilter(django_filters.FilterSet):

    class Meta:
        model = GVAIncident
        fields = ["date", "state", "tags"]
