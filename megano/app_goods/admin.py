from django.contrib import admin
from .models import Item


class ItemAdmin(admin.ModelAdmin):
    list_display = 'id', 'name'


admin.site.register(Item, ItemAdmin)
