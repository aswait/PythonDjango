from django import forms
from django.contrib.auth.models import Group
from django.core import validators

from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "name", "price", "description", "discount", "preview"

    images = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={"multiple": True})
    )


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ["name"]


class CSVImportForm(forms.Form):
    csv_file = forms.FileField()