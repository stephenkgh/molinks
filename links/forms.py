from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

from .models import Category, Link

class LinksForm(forms.Form):

    # user is required to populate category choice field
    def __init__(self, user, data=None, *args, **kwargs):
        assert isinstance(user, User), "This form class requires a User object as first argument"
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
    override = forms.BooleanField(required=False)

    # handle complex validation
    def clean(self):
        cleaned_data = super().clean()
        errors = []

        # validate URL unless overridden
        url = cleaned_data.get("url")
        override = cleaned_data.get("override")
        if not override:
            validate_url = URLValidator()
            try:
                validate_url(url)
            except ValidationError as e:
                errors.append(ValidationError("Enter a valid URL", code='bad_url'))

        # one of cat or new_cat are required
        if not (cleaned_data.get("category") or cleaned_data.get("new_cat")):
            errors.append(ValidationError("Choose an existing category or create a new one", code='no_cat'))

        # return multiple errors
        if errors:
            raise ValidationError(errors)


class EditCatForm(forms.Form):
    cat_ml = Category._meta.get_field('name').max_length

    name = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}), required=True, max_length=cat_ml)
