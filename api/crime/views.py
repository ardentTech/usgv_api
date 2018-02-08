from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from .models import GVAIncident
from .serializers import GVAIncidentSerializer


class GVAIncidentViewSet(ListModelMixin, GenericViewSet):

    queryset = GVAIncident.objects.all()
    serializer_class = GVAIncidentSerializer
