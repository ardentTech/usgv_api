from rest_framework import serializers

from .models import GVAIncident
from taxonomy.serializers import TagSerializer


class GVAIncidentSerializer(serializers.ModelSerializer):

    tags = TagSerializer(many=True)

    class Meta:
        fields = [
            "city_county", "date", "id", "injured", "killed", "state", "street", "tags", "url"]
        model = GVAIncident


class GVAIncidentStatsSerializer(serializers.ModelSerializer):

    year = serializers.IntegerField()

    class Meta:
        fields = ["injured", "killed", "state", "year"]
        model = GVAIncident
