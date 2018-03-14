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
            "url"]
        model = GVAIncident


class GVAIncidentStatsSerializer(serializers.ModelSerializer):

    state = serializers.IntegerField()
    year = serializers.IntegerField()

    class Meta:
        fields = ["incidents", "injured", "killed", "state", "year"]
        model = GVAIncident

    def to_representation(self, obj):
        obj["victims"] = obj["injured"] + obj["killed"]
        return obj
