from rest_framework import serializers

from .models import UsState


class UsStateSerializer(serializers.ModelSerializer):

    class Meta:
        fields = "__all__"
        model = UsState
