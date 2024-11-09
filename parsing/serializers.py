from rest_framework import serializers
from parsing import models
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth.models import User


class Register(AuthTokenSerializer):
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')


        if username and password:
            try:
                user = User()
                user.username = username
                user.set_password(password)
                user.save()
            except Exception as e:
                print(e)
                msg = "User already exists"
                raise serializers.ValidationError(msg, code='authorization')
        return super().validate(attrs)


class FetchItem(serializers.ModelSerializer):
    class Meta:
        model = models.FetchItem
        fields = ["url", "raw_json"]


class TagCloud(serializers.ModelSerializer):
    class Meta:
        model = models.TagCloud
        fields = ["tag"]


class Tag(serializers.ModelSerializer):   
    class Meta:
        model = models.Tag
        fields = ["name", "slug"]


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
    tags = Tag(many=True)
    images = Images(many=True)

    class Meta:
        model = models.Recipe
        exclude = ["foreign_id", "fetch_item"]
