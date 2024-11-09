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


class Images(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = ["image"]


class Recipes(serializers.ModelSerializer):
    images = Images(many=True)

    class Meta:
        model = models.Recipe
        fields = [
            "id",
            "name",
            "rating",
            "active_time",
            "prep_time",
            "total_time",
            "serving_size",
            "images",
        ]


class Recipe(serializers.ModelSerializer):
    tag_clouds = TagCloud(many=True)
    images = Images(many=True)

    class Meta:
        model = models.Recipe
        exclude = ["foreign_id", "fetch_item"]
