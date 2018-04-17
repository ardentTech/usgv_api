from rest_framework import serializers

from .models import GVAIncident


class GVAIncidentSerializer(serializers.ModelSerializer):

    class Meta:
        fields = [
            "city_county",
            "date",
            "id",
            "injured",
            "killed",
            "state",
            "street",
            "url",
            "victims"]
        model = GVAIncident
