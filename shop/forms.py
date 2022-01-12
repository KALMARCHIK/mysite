from django import forms

from shop.models import Item


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        exclude = ('sale', 'slug')
        widget = {'slug': forms.HiddenInput}
