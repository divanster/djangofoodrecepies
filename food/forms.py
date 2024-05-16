from ckeditor.widgets import CKEditorWidget
from django import forms
from .models import Item, Comment


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


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Add a comment...'}),
        }