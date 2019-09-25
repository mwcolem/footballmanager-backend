from rest_framework import serializers
from backend.models import PlayerModel

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerModel
        fields = '__all__'