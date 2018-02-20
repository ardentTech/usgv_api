from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from .models import UsState
from .serializers import UsStateSerializer


class UsStateViewSet(ListModelMixin, GenericViewSet):

    queryset = UsState.objects.all()
    serializer_class = UsStateSerializer
