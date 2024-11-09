from rest_framework import serializers
from parsing import models


class FetchItem(serializers.ModelSerializer):
    class Meta:
        model = models.FetchItem
        fields = ["url", "raw_json"]


class TagCloud(serializers.ModelSerializer):
    class Meta:
        model = models.TagCloud
        fields = ["tag"]

class Recipes(serializers.ModelSerializer):
    tag_clouds = TagCloud(many=True)

    class Meta:
        model = models.Recipe
        fields = ["id", "name", "tag_clouds"]
