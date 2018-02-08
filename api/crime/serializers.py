from rest_framework import serializers

from .models import GVAIncident


class GVAIncidentSerializer(serializers.ModelSerializer):

    class Meta:
        fields = "__all__"
        model = GVAIncident
