from django.contrib import admin

from parsing.models import FetchItem

@admin.register(FetchItem)
class FetchItemAdmin(admin.ModelAdmin):
    pass
