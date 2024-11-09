from django.urls import path
from parsing import views

urlpatterns = [
    path("fetch-item/", views.FetchItem.as_view()),
]