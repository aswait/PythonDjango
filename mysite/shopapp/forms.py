from django import forms
from django.contrib.auth.models import Group
from django.core import validators

from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "name", "price", "description", "discount"


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ["name"]
