from rest_framework import serializers

from .models import GVAIncident
from taxonomy.serializers import TagSerializer


class GVAIncidentSerializer(serializers.ModelSerializer):

    tags = TagSerializer(many=True)

    class Meta:
        fields = "__all__"
        model = GVAIncident
