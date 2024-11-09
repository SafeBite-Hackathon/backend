from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from mptt.admin import MPTTModelAdmin, TreeRelatedFieldListFilter
from parsing import models
from django.db.models import Count


@admin.register(models.FetchItem)
class FetchItemAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    raw_id_fields = ["fetch_item"]
    list_filter = (
        ('tags', TreeRelatedFieldListFilter),
    )


@admin.register(models.Tag)
class TagAdmin(MPTTModelAdmin):
    mptt_level_indent = 60

    list_display = ('name', 'recipe__count')

    def recipe__count(self, obj):
        return obj.recipe__count

    recipe__count.short_description = "Recipes total"
    recipe__count.admin_order_field = "recipe__count"

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        qs = super().get_queryset(request)
        return qs.annotate(Count("recipe"))


