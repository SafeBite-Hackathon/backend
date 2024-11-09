from rest_framework import generics, status, response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from parsing import serializers, models


class Login(ObtainAuthToken):
    pass


class Register(ObtainAuthToken):
    serializer_class = serializers.Register


class Profile(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.Profile

    def get(self, request, *args, **kwargs):
        serilazer = self.get_serializer(self.request.user)
        return response.Response(serilazer.data, status=status.HTTP_200_OK)


class FetchItem(generics.CreateAPIView):
    serializer_class = serializers.FetchItem

    def post(self, request, *args, **kwargs):
        url = request.data.get("url", None)
        if url is not None:
            try:
                instance = models.FetchItem.objects.get(url=url)
                serializer = self.get_serializer(instance, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return response.Response([url], status=status.HTTP_200_OK)
            except models.FetchItem.DoesNotExist:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                headers = self.get_success_headers(serializer.data)
                return response.Response([url], status=status.HTTP_201_CREATED, headers=headers)

        return response.Response(["url in body not found"], status=status.HTTP_400_BAD_REQUEST)

class Recipes(generics.ListAPIView):
    serializer_class = serializers.Recipes
    queryset = models.Recipe.objects.all()

class Recipe(generics.RetrieveAPIView):
    serializer_class = serializers.Recipe
    queryset = models.Recipe.objects.all()
