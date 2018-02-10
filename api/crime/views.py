from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from .filters import GVAIncidentFilter
from .models import GVAIncident
from .serializers import GVAIncidentSerializer


class GVAIncidentViewSet(ListModelMixin, GenericViewSet):

    filter_class = GVAIncidentFilter
    queryset = GVAIncident.objects.all()
    serializer_class = GVAIncidentSerializer
