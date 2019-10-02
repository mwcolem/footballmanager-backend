from backend.models import PlayerModel
from backend.serializers import PlayerSerializer
from rest_framework import generics
from . import scraper


class PlayerListCreate(generics.ListCreateAPIView):
    queryset = PlayerModel.objects.order_by('name')
    serializer_class = PlayerSerializer


class PlayerListUpdate(generics.ListCreateAPIView):
    scraper.update_players()
    queryset = PlayerModel.objects.order_by('name')
    serializer_class = PlayerSerializer
