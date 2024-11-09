from django.contrib import admin
from mptt.admin import MPTTModelAdmin, TreeRelatedFieldListFilter
from parsing import models


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
