from django.contrib import admin
from .models import Item, Rating

admin.site.register(Item)
admin.site.register(Rating)


class ItemAdmin(admin.ModelAdmin):
    list_display = ['item_name', 'item_desc', 'user_name', 'views']  # Display these fields in the admin panel
    list_filter = ['user_name', 'views']  # Add filters for these fields