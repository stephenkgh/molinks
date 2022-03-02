from django import forms
from django.contrib.auth.models import User

from .models import Category, Link

class LinksForm(forms.Form):

    # user is required to populate category choice field
    def __init__(self, user, data=None, *args, **kwargs):
        assert isinstance(user, User), "First argument to LinksForm must be a User object"
        super().__init__(data, *args, **kwargs)
        # __init__ happens after the attributes are built so we have to modify this queryset
        self.fields['category'].queryset = Category.objects.all(user)

    url_ml = Link._meta.get_field('url').max_length
    note_ml = Link._meta.get_field('note').max_length
    cat_ml = Category._meta.get_field('name').max_length

    url = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}), label='Link', required=True, max_length=url_ml)
    note = forms.CharField(label='Note', required=False, max_length=note_ml)
    category = forms.ModelChoiceField(queryset=None, required=False)
    new_cat = forms.CharField(label='or add new category', required=False, max_length=cat_ml)
