from rest_framework import generics
from parsing import serializers


class FetchItem(generics.CreateAPIView):
    serializer_class = serializers.FetchItem
