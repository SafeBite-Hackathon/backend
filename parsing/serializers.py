from rest_framework import serializers

from parsing.models import FetchItem

class FetchItem(serializers.ModelSerializer):
    class Meta:
        model = FetchItem
        fields = ["url", "raw_json"]
