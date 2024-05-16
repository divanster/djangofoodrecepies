from django.forms import ModelForm
from ckeditor.widgets import CKEditorWidget

from django.contrib import admin
from .models import Item


class ItemAdminForm(ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
        widgets = {
            'item_desc': CKEditorWidget(),  # Use CKEditorWidget for the item_desc field
        }


class ItemAdmin(admin.ModelAdmin):
    form = ItemAdminForm


admin.site.register(Item, ItemAdmin)
