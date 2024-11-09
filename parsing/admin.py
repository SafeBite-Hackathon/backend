from django.contrib import admin

from parsing import models

@admin.register(models.FetchItem)
class FetchItemAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    raw_id_fields = ["fetch_item"]