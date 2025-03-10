from django import forms
from import_export.forms import ConfirmImportForm, ImportForm

from .models import Part


class OrderImportForm(ImportForm):
    part = forms.ModelChoiceField(Part.objects)


class OrderConfirmImportForm(ConfirmImportForm):
    part = forms.ModelChoiceField(Part.objects)
