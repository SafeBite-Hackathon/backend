from django.urls import path
from parsing import views

urlpatterns = [
    path("fetch-item/", views.FetchItem.as_view()),
    path("recipes/", views.Recipes.as_view()),
    path("recipes/<int:pk>/", views.Recipe.as_view()),
]