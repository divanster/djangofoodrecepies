from ckeditor.widgets import CKEditorWidget
from django import forms
from .models import Item


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_name', 'item_desc', 'item_image']
        widgets = {
            'item_desc': CKEditorWidget()
        }

        labels = {
            'item_name': 'Заглавие',
            'item_desc': 'Описание',
            'item_image': 'Снимка'
        }
