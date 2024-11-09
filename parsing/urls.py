from django.urls import path
from parsing import views

urlpatterns = [
    path("login/", views.Login.as_view()),
    path("register/", views.Register.as_view()),
    path("fetch-item/", views.FetchItem.as_view()),
    path("recipes/", views.Recipes.as_view()),
    path("recipes/<int:pk>/", views.Recipe.as_view()),
]